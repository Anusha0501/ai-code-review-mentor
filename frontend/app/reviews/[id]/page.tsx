import { Nav } from "../../../components/ui/nav";

export default function ReviewDetailPage({ params }: { params: { id: string } }) {
  return <main className="min-h-screen p-8"><Nav /><section className="card mt-8 grid gap-6 p-8 lg:grid-cols-2"><div><h1 className="text-4xl font-semibold">Review {params.id}</h1><pre className="mt-6 rounded-2xl bg-black/50 p-5 text-sm text-emerald-300">+ validate webhook signatures{"\n"}+ add focused tests</pre></div><aside className="rounded-2xl border border-violet-400/30 p-5"><h2 className="text-2xl font-semibold">AI explanation panel</h2><p className="mt-3 text-zinc-300">Plain-English mentoring feedback appears here with suggested fixes and learning resources.</p></aside></section></main>;
}
