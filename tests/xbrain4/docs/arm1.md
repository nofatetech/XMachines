The goal of folding a t-shirt is
  a perfect long-term objective because it forces us to think about sequencing, precision, and state management, not just simple motor control.

  Here is my analysis of the request and the plan to implement the arm controller.

  Analysis

  Adding a robotic arm is a significant step up in complexity from the tank drive system. Here's a breakdown of the key challenges and how they
  fit into our existing architecture:

   1. State Management: The arm's state is more complex than the drive system. We need to track the angle of each joint and the status of the
      clamp (open/closed). This data should be stored in our central MachineState object in state.py to maintain a single source of truth.

   2. Kinematics (The "How to Move" Problem):
       * Joint Space vs. Task Space: For a simple 2-joint arm, we can start by controlling the angles of each joint directly (this is called
         Joint Space control). This is straightforward to implement.
       * The t-shirt folding goal, however, requires moving the clamp to a specific (X, Y) coordinate in space (this is Task Space). Translating
         from a desired (X, Y) position back to the required joint angles is a classic robotics problem called Inverse Kinematics (IK).
       * Our Approach: We will start by implementing direct joint control. This provides immediate functionality and a solid foundation. We will
         structure the code in a way that allows for an IK solver to be added later without a major refactor.

   3. Hardware Abstraction: Just like with the DC and stepper motors, we need a clear separation between the simulated arm and the real
      GPIO-based arm. We will create a new arm.py module and use an AbstractArmController to define a standard interface, with
      SimulatedArmController and GPIOArmController as concrete implementations. Servo motors are the best choice for this, and gpiozero has
      excellent Servo support.

   4. Command and Control: The simple linear and angular commands won't work for the arm. We need a new command structure. A good approach is a
      JSON object that can specify the target state for different parts of the arm, for example: {"arm_target": {"joint1": 45, "joint2": -30,
      "clamp": 1}}. We can adapt our UDP server to handle this new command type. For more complex, multi-step actions like "fold," a FastAPI
      endpoint will be more suitable in the future.

  The Plan

  I will implement the arm controller in five stages, following the established patterns in the codebase.

   1. Update State (`state.py`):
       * I will first update MachineState to include a dictionary for the arm's status, tracking the angle of each joint and the clamp's state
         (e.g., 0 for closed, 1 for open).

   2. Create Arm Controller Module (`arm.py`):
       * I will create a new file, arm.py.
       * Inside, I'll define an AbstractArmController with methods like set_pose(joint1, joint2, clamp) and stop().
       * I will implement SimulatedArmController, which will simply log the angles it's commanded to move to.
       * I will implement GPIOArmController, which will use the gpiozero.Servo class to control the physical servo motors for the two joints and
         the clamp.

   3. Add Configuration (`.env.example`):
       * I will add new environment variables to .env.example for the GPIO pins connected to the arm's servo motors (e.g., JOINT1_PIN,
         JOINT2_PIN, CLAMP_PIN).

   4. Integrate into Main Application (`main.py`):
       * I will create a new factory function, create_arm_controller, which reads the environment and instantiates the correct arm controller
         (Simulated or GPIO).
       * I will call this factory in the main execution block to create an arm object.

   5. Update UDP Command Server (`udp_comm.py`):
       * I will modify the poll method in UDPServer. It will now check incoming JSON messages for a new "arm_target" key.
       * If this key is present, it will parse the dictionary of joint/clamp targets and call the arm.set_pose() method with the specified
         values.

  This plan establishes a robust, extensible foundation for all future arm development, starting with direct joint control and paving the way for
  more advanced capabilities like Inverse Kinematics and sequenced actions.