'use client';

import React, { useState } from 'react';
import { motion } from 'motion/react';

export function Day5WelcomeView({ onStart }: { onStart: () => void }) {
  const [selectedUseCase, setSelectedUseCase] = useState<string>('');

  const useCases = [
    { id: 'ecommerce', label: 'E-Commerce Store', icon: '🛍️' },
    { id: 'saas', label: 'SaaS Platform', icon: '💻' },
    { id: 'subscription', label: 'Subscription Business', icon: '🔄' },
    { id: 'marketplace', label: 'Marketplace', icon: '🏪' },
    { id: 'other', label: 'Other', icon: '❓' },
  ];

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-2xl w-full"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="text-6xl mb-4"
          >
            💳
          </motion.div>
          <h1 className="text-4xl font-bold text-white mb-2">Razorpay SDR</h1>
          <p className="text-xl text-slate-300">Sales Development Representative</p>
          <p className="text-sm text-slate-400 mt-2">Let's discuss how Razorpay can help your business accept payments</p>
        </div>

        {/* Company Info Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="bg-linear-to-r from-slate-800/50 to-slate-800/30 backdrop-blur-lg rounded-2xl border border-slate-700/50 p-6 mb-8"
        >
          <h2 className="text-lg font-semibold text-white mb-3">About Razorpay</h2>
          <p className="text-slate-300 text-sm leading-relaxed">
            India's leading payments platform helping 500,000+ businesses accept online payments. 
            We support credit cards, debit cards, UPI, net banking, and digital wallets.
          </p>
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="bg-slate-900/50 rounded-lg p-3">
              <p className="text-slate-400 text-xs">Setup Fee</p>
              <p className="text-white font-bold text-lg">FREE</p>
            </div>
            <div className="bg-slate-900/50 rounded-lg p-3">
              <p className="text-slate-400 text-xs">Commission</p>
              <p className="text-white font-bold text-lg">1-2% + GST</p>
            </div>
          </div>
        </motion.div>

        {/* Use Case Selection */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="mb-8"
        >
          <p className="text-slate-300 text-sm font-medium mb-4">What's your business type?</p>
          <div className="grid grid-cols-2 gap-3">
            {useCases.map((useCase, idx) => (
              <motion.button
                key={useCase.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + idx * 0.1 }}
                onClick={() => setSelectedUseCase(useCase.id)}
                className={`p-4 rounded-lg border transition-all ${
                  selectedUseCase === useCase.id
                    ? 'bg-blue-600/30 border-blue-500 shadow-lg shadow-blue-500/20'
                    : 'bg-slate-800/30 border-slate-700 hover:border-slate-600'
                }`}
              >
                <div className="text-2xl mb-2">{useCase.icon}</div>
                <p className="text-white text-sm font-medium">{useCase.label}</p>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.5 }}
          className="grid grid-cols-3 gap-4 mb-8"
        >
          <div className="text-center">
            <div className="text-3xl mb-2">🎯</div>
            <p className="text-white font-semibold text-sm">Expert Advice</p>
            <p className="text-slate-400 text-xs mt-1">Personalized guidance</p>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-2">⚡</div>
            <p className="text-white font-semibold text-sm">Quick Setup</p>
            <p className="text-slate-400 text-xs mt-1">Start in minutes</p>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-2">🔒</div>
            <p className="text-white font-semibold text-sm">Secure</p>
            <p className="text-slate-400 text-xs mt-1">PCI DSS Level 1</p>
          </div>
        </motion.div>

        {/* CTA Button */}
        <motion.button
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.5 }}
          onClick={onStart}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full bg-linear-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold py-4 rounded-lg transition-all shadow-lg shadow-blue-500/30"
        >
          Start Sales Call 🚀
        </motion.button>

        {/* Footer */}
        <p className="text-center text-slate-500 text-xs mt-6">
          Questions? Our team is here to help. Let's connect!
        </p>
      </motion.div>
    </div>
  );
}
