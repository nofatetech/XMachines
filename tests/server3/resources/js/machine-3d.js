import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

class Machine3D {
    constructor(container) {
        this.container = container;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.model = null;

        this.init();
    }

    init() {
        // Renderer
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);

        // Camera and Controls
        this.camera.position.set(0, 2, 4);
        this.controls.enableDamping = true;

        // Lighting
        this.scene.background = new THREE.Color(0x4a5568);
        this.scene.add(new THREE.HemisphereLight(0xffffbb, 0x080820, 1.5));
        const dirLight = new THREE.DirectionalLight(0xffffff, 1);
        dirLight.position.set(3, 5, 4);
        this.scene.add(dirLight);

        // Model
        this.model = this.createMachineModel();
        this.model.position.y = 0.75;
        this.scene.add(this.model);

        // Event Listeners
        window.addEventListener('resize', this.onWindowResize.bind(this), false);

        this.animate();
    }

    createMachineModel() {
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

        return group;
    }

    updateState(machine) {
        if (!this.model) return;

        // Update beacon color
        this.model.beacon.material.color.setHex(machine.is_online ? 0x00ff00 : 0xff0000);

        // Update wheel rotation
        const rotationSpeed = (machine.motor_left_speed + machine.motor_right_speed) / 200; // Average and normalize
        this.model.wheels.forEach(wheel => {
            wheel.rotation.x += rotationSpeed;
        });
    }

    onWindowResize() {
        if (!this.container) return;
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
}

export default Machine3D;
