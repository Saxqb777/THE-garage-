'use client';

import dynamic from 'next/dynamic';

// three.js needs the browser, so the scene and the HUD skip server rendering entirely.
const Experience = dynamic(() => import('@/scene/Experience'), { ssr: false });
const Hud = dynamic(() => import('@/ui/Hud'), { ssr: false });
const HoverLabel = dynamic(() => import('@/ui/HoverLabel'), { ssr: false });
const PartCard = dynamic(() => import('@/ui/PartCard'), { ssr: false });
const Dash = dynamic(() => import('@/ui/Dash'), { ssr: false });
const ExplodeBar = dynamic(() => import('@/ui/ExplodeBar'), { ssr: false });
const Search = dynamic(() => import('@/ui/Search'), { ssr: false });
const CatalogLoader = dynamic(() => import('@/ui/CatalogLoader'), { ssr: false });

export default function Home() {
  return (
    <main className="stage">
      <Experience />
      <Hud />
      <PartCard />
      <Dash />
      <ExplodeBar />
      <Search />
      <CatalogLoader />
      <HoverLabel />
    </main>
  );
}
