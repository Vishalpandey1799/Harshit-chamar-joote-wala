'use client';

import { useEffect, useState } from 'react';

export interface TutorSessionViewProps {
  mode?: string;
  voice?: string;
  concept?: string;
}

export const TutorSessionView = ({
  mode = 'select',
  voice = 'matthew',
  concept = '',
}: TutorSessionViewProps) => {
  const [displayMode, setDisplayMode] = useState(mode);
  const [displayVoice, setDisplayVoice] = useState(voice);
  const [displayConcept, setDisplayConcept] = useState(concept);

  useEffect(() => {
    setDisplayMode(mode);
    setDisplayVoice(voice);
    setDisplayConcept(concept);
  }, [mode, voice, concept]);

  const getModeConfig = (currentMode: string) => {
    const configs: Record<
      string,
      {
        label: string;
        color: string;
        bgColor: string;
        icon: string;
        description: string;
      }
    > = {
      select: {
        label: '📚 Choose Mode',
        color: 'text-purple-600',
        bgColor: 'bg-purple-50',
        icon: '🎯',
        description: 'Select your learning mode and concept',
      },
      learn: {
        label: '📖 Learn Mode',
        color: 'text-blue-600',
        bgColor: 'bg-blue-50',
        icon: '🧑‍🏫',
        description: 'Listen to concept explanation',
      },
      quiz: {
        label: '❓ Quiz Mode',
        color: 'text-amber-600',
        bgColor: 'bg-amber-50',
        icon: '🎓',
        description: 'Answer questions to test understanding',
      },
      teach_back: {
        label: '💬 Teach Back Mode',
        color: 'text-green-600',
        bgColor: 'bg-green-50',
        icon: '👨‍🎓',
        description: 'Explain the concept to the tutor',
      },
    };

    return configs[currentMode] || configs['select'];
  };

  const getVoiceConfig = (currentVoice: string) => {
    const configs: Record<
      string,
      { name: string; emoji: string; color: string }
    > = {
      matthew: {
        name: 'Matthew',
        emoji: '👨‍🏫',
        color: 'text-blue-500',
      },
      alicia: {
        name: 'Alicia',
        emoji: '👩‍💼',
        color: 'text-pink-500',
      },
      ken: {
        name: 'Ken',
        emoji: '👨‍💻',
        color: 'text-emerald-500',
      },
    };

    const voiceKey = currentVoice.toLowerCase().includes('alicia')
      ? 'alicia'
      : currentVoice.toLowerCase().includes('ken')
        ? 'ken'
        : 'matthew';

    return configs[voiceKey];
  };

  const modeConfig = getModeConfig(displayMode);
  const voiceConfig = getVoiceConfig(displayVoice);

  return (
    <div className="w-full h-full flex flex-col items-center justify-center gap-8 p-8 bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="text-6xl animate-bounce">{modeConfig.icon}</div>
        <h1 className="text-4xl font-bold text-white">{modeConfig.label}</h1>
        <p className="text-lg text-slate-300">{modeConfig.description}</p>
      </div>

      {/* Main Status Card */}
      <div
        className={`w-full max-w-2xl rounded-2xl border-2 p-8 backdrop-blur-md ${modeConfig.bgColor} border-current shadow-2xl`}
      >
        <div className="space-y-6">
          {/* Concept Display */}
          {displayConcept && (
            <div className="space-y-2">
              <label className="text-sm font-semibold text-slate-600 uppercase tracking-wider">
                📚 Current Concept
              </label>
              <div className="text-2xl font-bold text-slate-800 capitalize">
                {displayConcept}
              </div>
            </div>
          )}

          {/* Mode Status */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2 bg-white/50 rounded-lg p-4">
              <label className="text-sm font-semibold text-slate-600 uppercase tracking-wider">
                🎯 Learning Mode
              </label>
              <div className={`text-xl font-bold capitalize ${modeConfig.color}`}>
                {displayMode === 'teach_back' ? 'Teach Back' : displayMode}
              </div>
            </div>

            <div className="space-y-2 bg-white/50 rounded-lg p-4">
              <label className="text-sm font-semibold text-slate-600 uppercase tracking-wider">
                🎙️ Voice
              </label>
              <div className={`text-xl font-bold ${voiceConfig.color} flex items-center gap-2`}>
                <span>{voiceConfig.emoji}</span>
                <span>{voiceConfig.name}</span>
              </div>
            </div>
          </div>

          {/* Mode Description */}
          <div className="bg-white/70 rounded-lg p-4 border-l-4 border-current">
            <p className="text-sm text-slate-700 leading-relaxed">
              {displayMode === 'learn' &&
                'Listen carefully as the tutor explains the concept with clear examples and real-world applications.'}
              {displayMode === 'quiz' &&
                'Answer the questions thoughtfully. The tutor will provide feedback and guide you through any misconceptions.'}
              {displayMode === 'teach_back' &&
                'Explain the concept in your own words as if teaching someone new. The tutor will give constructive feedback.'}
              {displayMode === 'select' &&
                'Choose a learning mode (Learn, Quiz, or Teach Back) and pick a concept to get started!'}
            </p>
          </div>
        </div>
      </div>

      {/* Mode Indicators */}
      <div className="w-full max-w-2xl flex gap-3 justify-center flex-wrap">
        {['learn', 'quiz', 'teach_back'].map((m) => (
          <div
            key={m}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all ${
              displayMode === m
                ? 'bg-white text-blue-600 shadow-lg scale-105'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            {m === 'teach_back' ? '💬 Teach Back' : `${m.charAt(0).toUpperCase()}${m.slice(1)}`}
          </div>
        ))}
      </div>

      {/* Listening Indicator */}
      <div className="flex items-center gap-2 text-white">
        <div className="flex gap-1">
          <div className="w-2 h-6 bg-white rounded-full animate-pulse"></div>
          <div className="w-2 h-6 bg-white rounded-full animate-pulse delay-100"></div>
          <div className="w-2 h-6 bg-white rounded-full animate-pulse delay-200"></div>
        </div>
        <span className="text-sm">Listening...</span>
      </div>
    </div>
  );
};
