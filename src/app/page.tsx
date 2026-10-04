'use client';

import dynamic from 'next/dynamic';

// three.js needs the browser, so the scene and the HUD skip server rendering entirely.
const Experience = dynamic(() => import('@/scene/Experience'), { ssr: false });
const Hud = dynamic(() => import('@/ui/Hud'), { ssr: false });

export default function Home() {
  return (
    <main className="stage">
      <Experience />
      <Hud />
    </main>
  );
}
