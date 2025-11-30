import { ShoppingBag, Package, Tag, ShoppingCart, Store } from "lucide-react";
import { Button } from "@/components/livekit/button";

export default function WelcomeView({ startButtonText = "Start Shopping", onStartCall }: any) {
  return (
    <div
      className="bg-gradient-to-b from-gray-950 via-black to-gray-900 text-gray-200 min-h-screen overflow-y-auto py-12 px-4"
    >
      <div className="flex flex-col items-center mx-auto max-w-5xl">
        <header className="w-full flex justify-start items-center py-4">
          <div className="flex items-center space-x-2">
            <Store className="text-pink-400" size={26} />
            <span className="text-lg font-bold text-gray-300">ShopEase by Myntra</span>
          </div>
        </header>

        <section className="flex flex-col items-center text-center w-full max-w-4xl pt-10">
          <div className="mb-8 text-green-400">
            <ShoppingBag size={80} className="animate-pulse" />
          </div>

          <h1 className="text-5xl sm:text-6xl font-extrabold text-white mb-3 tracking-tight">
            Voice-Driven Shopping
          </h1>

          <p className="text-lg sm:text-xl text-gray-300 max-w-xl font-medium mb-16">
            Browse products, filter by voice, and place orders — all through a conversational assistant.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-16">
            <div className="bg-gray-800/40 border border-gray-700/60 rounded-2xl p-6 flex flex-col items-center text-center backdrop-blur-md shadow-xl hover:scale-[1.03] transition-all cursor-pointer">
              <Package size={48} className="text-blue-300 mb-3" />
              <p className="text-lg font-bold text-white mb-1">Browse Catalog</p>
              <p className="text-xs text-blue-200 max-w-[90%]">Explore mugs, hoodies, t-shirts and more from the catalog.</p>
            </div>

            <div className="bg-gray-800/40 border border-gray-700/60 rounded-2xl p-6 flex flex-col items-center text-center backdrop-blur-md shadow-xl hover:scale-[1.03] transition-all cursor-pointer">
              <Tag size={48} className="text-yellow-300 mb-3" />
              <p className="text-lg font-bold text-white mb-1">Smart Filters</p>
              <p className="text-xs text-yellow-200 max-w-[90%]">Ask by color, size, price or category to narrow things down.</p>
            </div>

            <div className="bg-gray-800/40 border border-gray-700/60 rounded-2xl p-6 flex flex-col items-center text-center backdrop-blur-md shadow-xl hover:scale-[1.03] transition-all cursor-pointer">
              <ShoppingCart size={48} className="text-green-300 mb-3" />
              <p className="text-lg font-bold text-white mb-1">Voice Ordering</p>
              <p className="text-xs text-green-200 max-w-[90%]">Say what you want to buy and get an order created instantly.</p>
            </div>
          </div>

          <div className="w-full max-w-2xl mb-12">
            <p className="mb-6 font-semibold text-gray-400">Popular categories:</p>
            <div className="flex gap-3 flex-wrap justify-center">
              {["Hoodies", "T-Shirts", "Mugs", "Shoes", "Accessories"].map((cat) => (
                <span key={cat} className="px-4 py-2 bg-gray-700/50 border border-gray-600/70 rounded-full text-sm font-medium text-gray-200 shadow-sm">
                  {cat}
                </span>
              ))}
            </div>
          </div>

          <Button
            variant="primary"
            size="lg"
            onClick={onStartCall}
            className="w-full sm:w-80 font-bold text-xl py-4 bg-pink-500 hover:bg-pink-400 text-black shadow-2xl shadow-pink-500/40 hover:shadow-pink-400/70 transition-all hover:-translate-y-1 active:translate-y-0"
          >
            {startButtonText}
          </Button>

          <div className="mt-10 mb-12 text-gray-500 text-xs sm:text-sm">
            <p>Murf Falcon TTS • Gemini • Deepgram • LiveKit Agents</p>
          </div>
        </section>

        <footer className="w-full py-4 text-center text-gray-600 text-xs max-w-xl px-4">
          <p>This is a voice-driven shopping experience. Speak clearly when prompted.</p>
        </footer>
      </div>
    </div>
  );
}
