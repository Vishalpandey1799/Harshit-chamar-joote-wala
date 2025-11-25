import { Button } from '@/components/livekit/button';

function WelcomeImage() {
  return (
    <div className="text-7xl mb-6 animate-bounce">🎓</div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref}>
      <section className="bg-linear-to-br from-slate-950 via-blue-950 to-slate-950 flex flex-col items-center justify-center text-center min-h-screen">
        <WelcomeImage />

        <h1 className="text-5xl font-bold text-white mb-2">
          Teach-the-Tutor
        </h1>

        <p className="text-blue-200 max-w-prose pt-3 leading-7 font-medium text-lg mb-4">
          Master programming concepts through interactive learning modes
        </p>

        <div className="grid grid-cols-3 gap-4 max-w-2xl my-8">
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 backdrop-blur">
            <div className="text-3xl mb-2">📖</div>
            <p className="text-white font-semibold text-sm">Learn</p>
            <p className="text-blue-200 text-xs mt-1">Get concept explanations</p>
          </div>
          <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-4 backdrop-blur">
            <div className="text-3xl mb-2">❓</div>
            <p className="text-white font-semibold text-sm">Quiz</p>
            <p className="text-amber-200 text-xs mt-1">Test your understanding</p>
          </div>
          <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4 backdrop-blur">
            <div className="text-3xl mb-2">💬</div>
            <p className="text-white font-semibold text-sm">Teach Back</p>
            <p className="text-green-200 text-xs mt-1">Explain to the tutor</p>
          </div>
        </div>

        <div className="mb-8 text-white text-sm">
          <p className="mb-3 font-semibold">Choose from these concepts:</p>
          <div className="flex gap-2 justify-center flex-wrap max-w-2xl">
            {['Variables', 'Loops', 'Functions', 'Arrays', 'Conditionals'].map((concept) => (
              <span key={concept} className="px-3 py-1 bg-indigo-500/20 border border-indigo-500/50 rounded-full text-xs">
                📚 {concept}
              </span>
            ))}
          </div>
        </div>

        <Button variant="primary" size="lg" onClick={onStartCall} className="mt-6 w-64 font-mono text-base">
          {startButtonText}
        </Button>

        <div className="mt-8 text-blue-300 text-sm">
          <p>Powered by AI Tutor with Voice • Murf.AI's falcon tts • Google Gemini and deepgram for stt</p>
        </div>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center">
        <p className="text-slate-400 max-w-prose pt-1 text-xs leading-5 font-normal text-pretty md:text-sm">
          Built with LiveKit Agents • Active Recall Learning • Multi-mode Training
        </p>
      </div>
    </div>
  );
};
