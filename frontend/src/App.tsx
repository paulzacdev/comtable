import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Sphere, MeshDistortMaterial, Float, Text, MeshWobbleMaterial } from '@react-three/drei';
import { motion } from 'framer-motion';
import { LayoutDashboard, FileText, ShieldCheck, Cpu, Monitor, Settings } from 'lucide-react';
import axios from 'axios';

// --- 3D Components ---

const FuturisticCore = () => {
  return (
    <Float speed={2} rotationIntensity={1} floatIntensity={2}>
      <Sphere args={[1, 64, 64]}>
        <MeshDistortMaterial color="#00f2ff" speed={2} distort={0.4} radius={1} />
      </Sphere>
    </Float>
  );
};

const FloatingPanel = ({ position, text, color = "#00f2ff" }) => {
  return (
    <Float speed={1.5} rotationIntensity={0.5} floatIntensity={1}>
      <mesh position={position}>
        <boxGeometry args={[2, 1.2, 0.1]} />
        <meshStandardMaterial color="#111" transparent opacity={0.8} roughness={0} metalness={1} />
        <Text
          position={[0, 0, 0.06]}
          fontSize={0.2}
          color={color}
          font="https://fonts.gstatic.com/s/robotoslab/v7/L0RkwS9_zXn7W90e1S9Y9S.woff"
        >
          {text}
        </Text>
      </mesh>
    </Float>
  );
};

// --- Main Interface ---

const App = () => {
  const executeAction = async (action) => {
    try {
      const res = await axios.post('http://localhost:8000/api/execute', {
        command_id: 'user_trigger',
        action: action
      });
      alert(`System: ${res.data.status} - ${action}`);
    } catch (e) {
      alert(`Error: ${e.message}`);
    }
  };

  return (
    <div className="h-screen w-screen bg-black text-cyan-400 overflow-hidden font-mono relative">
      {/* 3D Background Canvas */}
      <div className="absolute inset-0 z-0">
        <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
          <color attach="background" args={['#020205']} />
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} intensity={1} />
          <spotLight position={[-10, 10, 10]} angle={0.15} penumbra={1} intensity={2} />

          <FuturisticCore />
          <FloatingPanel position={[-3, 1, 0]} text="AI COLLECTOR: ACTIVE" />
          <FloatingPanel position={[3, 1, 0]} text="AUDITOR: SCANNING" color="#ff00ea" />
          <FloatingPanel position={[0, -2, 0]} text="SYSTEM BRIDGE: CONNECTED" color="#00ff41" />

          <OrbitControls enableZoom={false} />
        </Canvas>
      </div>

      {/* HUD UI Layer */}
      <div className="absolute inset-0 z-10 pointer-events-none flex flex-col justify-between p-8">
        {/* Top Header */}
        <header className="flex justify-between items-center pointer-events-auto">
          <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="bg-cyan-900/30 backdrop-blur-md border border-cyan-500/50 p-4 rounded-br-3xl rounded-tl-xl"
          >
            <h1 className="text-2xl font-bold tracking-tighter flex items-center gap-2">
              <Cpu className="animate-pulse" /> ACCOUNTING-AI OS <span className="text-xs bg-cyan-500 text-black px-2 py-1 rounded">v1.0.0-BETA</span>
            </h1>
          </motion.div>
          <div className="flex gap-4">
            <button className="p-3 bg-cyan-900/30 border border-cyan-500/50 rounded-full hover:bg-cyan-500 hover:text-black transition-all">
              <Settings size={20} />
            </button>
          </div>
        </header>

        {/* Side Controls (PC Bridge) */}
        <div className="flex justify-between items-end h-full">
          <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="pointer-events-auto space-y-4 bg-cyan-900/20 backdrop-blur-lg border border-cyan-500/30 p-6 rounded-tr-3xl rounded-bl-xl"
          >
            <h3 className="text-xs font-bold uppercase opacity-50 mb-4">Remote PC Control</h3>
            <button onClick={() => executeAction('open_calculator')} className="w-full flex items-center gap-3 p-3 bg-cyan-500/10 border border-cyan-500/50 rounded-lg hover:bg-cyan-500/30 transition-all group">
              <Monitor size={18} className="group-hover:rotate-12 transition-transform" />
              <span>Launch Calculator</span>
            </button>
            <button onClick={() => executeAction('open_notepad')} className="w-full flex items-center gap-3 p-3 bg-cyan-500/10 border border-cyan-500/50 rounded-lg hover:bg-cyan-500/30 transition-all group">
              <FileText size={18} className="group-hover:rotate-12 transition-transform" />
              <span>Open Notepad</span>
            </button>
            <button onClick={() => executeAction('open_explorer')} className="w-full flex items-center gap-3 p-3 bg-cyan-500/10 border border-cyan-500/50 rounded-lg hover:bg-cyan-500/30 transition-all group">
              <LayoutDashboard size={18} className="group-hover:rotate-12 transition-transform" />
              <span>File Explorer</span>
            </button>
          </motion.div>

          <motion.div
            initial={{ x: 100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="pointer-events-auto space-y-4 bg-cyan-900/20 backdrop-blur-lg border border-cyan-500/30 p-6 rounded-tl-3xl rounded-br-xl"
          >
            <h3 className="text-xs font-bold uppercase opacity-50 mb-4">AI Agency Status</h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-sm">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-ping" />
                <span>Collector: Idle</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <div className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse" />
                <span>Auditor: Processing</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <div className="w-2 h-2 rounded-full bg-cyan-500 animate-bounce" />
                <span>Analyst: Ready</span>
              </div>
            </div>
            <div className="mt-6 p-4 bg-black/40 border border-cyan-500/20 rounded-lg">
              <p className="text-[10px] opacity-60 mb-2">SYSTEM LOG</p>
              <p className="text-xs italic">"Awaiting authorized input from accountant..."</p>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default App;
