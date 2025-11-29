import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

class SharedScene {
    constructor(container) {
        this.container = container;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.labelRenderer = new CSS2DRenderer();
        this.controls = new OrbitControls(this.camera, this.labelRenderer.domElement);
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        this.machineModels = new Map();

        this.init();
    }

    init() {
        // Main renderer
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);

        // Label renderer
        this.labelRenderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.labelRenderer.domElement.style.position = 'absolute';
        this.labelRenderer.domElement.style.top = '0px';
        this.container.appendChild(this.labelRenderer.domElement);

        // Camera and controls
        this.camera.position.set(0, 5, 10);
        this.controls.enableDamping = true;

        // Lighting
        this.scene.background = new THREE.Color(0x1a202c);
        this.scene.add(new THREE.HemisphereLight(0xffffbb, 0x080820, 1.5));
        const dirLight = new THREE.DirectionalLight(0xffffff, 1);
        dirLight.position.set(5, 10, 7.5);
        this.scene.add(dirLight);

        // Ground plane
        const ground = new THREE.Mesh(
            new THREE.PlaneGeometry(100, 100),
            new THREE.MeshStandardMaterial({ color: 0x4a5568 })
        );
        ground.rotation.x = -Math.PI / 2;
        this.scene.add(ground);

        // Event Listeners
        window.addEventListener('resize', this.onWindowResize.bind(this), false);
        this.labelRenderer.domElement.addEventListener('click', this.onMouseClick.bind(this), false);

        this.animate();
    }

    createMachineModel(machine) {
        const group = new THREE.Group();

        // Body
        const bodyMaterial = new THREE.MeshStandardMaterial({ color: 0x808080, roughness: 0.5, metalness: 0.8 });
        const body = new THREE.Mesh(new THREE.BoxGeometry(2, 1, 3), bodyMaterial);
        group.add(body);

        // Wheels
        const wheelGeometry = new THREE.CylinderGeometry(0.5, 0.5, 0.3, 32);
        const wheelMaterial = new THREE.MeshStandardMaterial({ color: 0x1a202c, roughness: 0.8 });
        const wheels = [
            new THREE.Mesh(wheelGeometry, wheelMaterial),
            new THREE.Mesh(wheelGeometry, wheelMaterial),
            new THREE.Mesh(wheelGeometry, wheelMaterial),
            new THREE.Mesh(wheelGeometry, wheelMaterial)
        ];
        wheels[0].position.set(1.2, -0.2, 1);
        wheels[1].position.set(-1.2, -0.2, 1);
        wheels[2].position.set(1.2, -0.2, -1);
        wheels[3].position.set(-1.2, -0.2, -1);
        wheels.forEach(wheel => {
            wheel.rotation.z = Math.PI / 2;
            group.add(wheel);
        });
        group.wheels = wheels;

        // Status Beacon
        const beaconGeometry = new THREE.SphereGeometry(0.2, 16, 16);
        const beaconMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 }); // Default red
        const beacon = new THREE.Mesh(beaconGeometry, beaconMaterial);
        beacon.position.y = 1;
        group.add(beacon);
        group.beacon = beacon;

        // Label
        const labelDiv = document.createElement('div');
        labelDiv.className = 'machine-label';
        labelDiv.textContent = machine.name;
        const label = new CSS2DObject(labelDiv);
        label.position.set(0, 2, 0);
        group.add(label);

        group.userData = { id: machine.id };

        return group;
    }

    populateScene(machines) {
        machines.forEach((machine, index) => {
            const model = this.createMachineModel(machine);
            model.position.set(index * 5 - (machines.length - 1) * 2.5, 0.75, 0);
            this.scene.add(model);
            this.machineModels.set(machine.id, model);
            this.updateMachineState(machine);
        });
    }

    updateMachineState(machine) {
        const model = this.machineModels.get(machine.id);
        if (!model) return;

        // Update beacon color
        model.beacon.material.color.setHex(machine.is_online ? 0x00ff00 : 0xff0000);

        // Update wheel rotation
        const rotationSpeed = (machine.motor_left_speed + machine.motor_right_speed) / 200; // Average and normalize
        model.wheels.forEach(wheel => {
            wheel.rotation.x += rotationSpeed;
        });
    }

    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.labelRenderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    onMouseClick(event) {
        this.mouse.x = (event.clientX / this.renderer.domElement.clientWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / this.renderer.domElement.clientHeight) * 2 + 1;
        this.raycaster.setFromCamera(this.mouse, this.camera);

        const intersects = this.raycaster.intersectObjects(this.scene.children, true);
        if (intersects.length > 0) {
            let clickedObject = intersects[0].object;
            while (clickedObject.parent && !clickedObject.userData.id) {
                clickedObject = clickedObject.parent;
            }

            if (clickedObject.userData.id) {
                const event = new CustomEvent('machine-selected', { detail: { id: clickedObject.userData.id } });
                window.dispatchEvent(event);
            }
        }
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
        this.labelRenderer.render(this.scene, this.camera);
    }
}

export default SharedScene;
