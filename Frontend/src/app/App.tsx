import { useState } from 'react';
import { Sparkles, Gift, Send, Star, Heart, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

interface Joke {
  id: number;
  text: string;
  emoji: string;
  hiddenMeaning: string;
}

const sampleJokes: Joke[] = [];

function FloatingDecoration({ type, delay = 0 }: { type: 'bubble' | 'star' | 'heart' | 'sparkle', delay?: number }) {
  const icons = {
    bubble: '○',
    star: '✦',
    heart: '♥',
    sparkle: '✨'
  };

  const colors = [
    'text-[#ffc0e3]',
    'text-[#e0c3fc]',
    'text-[#c3dbf7]',
    'text-[#c3f7e2]',
    'text-[#ffd5b8]'
  ];

  const randomColor = colors[Math.floor(Math.random() * colors.length)];
  const randomX = Math.random() * 100;
  const randomDuration = 15 + Math.random() * 10;

  return (
    <motion.div
      className={`absolute ${randomColor} opacity-30 pointer-events-none select-none`}
      style={{
        left: `${randomX}%`,
        fontSize: type === 'bubble' ? '3rem' : '1.5rem'
      }}
      initial={{ y: '100vh', rotate: 0, opacity: 0 }}
      animate={{
        y: '-100vh',
        rotate: 360,
        opacity: [0, 0.5, 0.3, 0]
      }}
      transition={{
        duration: randomDuration,
        delay: delay,
        repeat: Infinity,
        ease: 'linear'
      }}
    >
      {icons[type]}
    </motion.div>
  );
}

function JokeCard({ joke }: { joke: Joke }) {
  const [isRevealed, setIsRevealed] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.5, type: 'spring' }}
      className="mb-4"
    >
      <div className="relative">
        <div className="bg-gradient-to-br from-[#ffc0e3]/20 via-[#e0c3fc]/20 to-[#c3dbf7]/20 backdrop-blur-sm rounded-[2rem] p-6 pr-20 shadow-lg border-2 border-white/40">
          <div className="flex items-start gap-3">
            <span className="text-4xl flex-shrink-0">{joke.emoji}</span>
            <p className="text-[#4a4063] leading-relaxed font-medium">
              {joke.text}
            </p>
          </div>

          {/* Decorative sparkles */}
          <div className="absolute -top-2 -left-2">
            <Star className="w-5 h-5 text-[#ffc0e3] animate-pulse" style={{ animationDelay: '0.5s' }} />
          </div>

          {/* Gift Box Button in Corner */}
          <motion.button
            onClick={() => setIsRevealed(!isRevealed)}
            className="absolute top-4 right-4 group cursor-pointer"
            whileHover={{ scale: 1.1, rotate: 5 }}
            whileTap={{ scale: 0.9 }}
            title={isRevealed ? 'Hide Secret' : 'Reveal Hidden Meaning'}
          >
            {/* Gift Box */}
            <div className="relative">
              {/* Box body */}
              <div className="w-14 h-14 bg-gradient-to-br from-[#ffc0e3] to-[#e0c3fc] rounded-2xl shadow-lg border-2 border-white/60 flex items-center justify-center">
                <Gift className="w-7 h-7 text-white drop-shadow-sm" />
              </div>
              {/* Ribbon bow on top */}
              <div className="absolute -top-2 left-1/2 -translate-x-1/2">
                <div className="w-6 h-3 bg-gradient-to-r from-[#f9d58f] to-[#fbbf24] rounded-full shadow-md" />
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-1 h-4 bg-gradient-to-b from-[#f9d58f] to-transparent" />
              </div>
              {/* Sparkle effect */}
              <motion.div
                className="absolute -top-1 -right-1"
                animate={{
                  scale: [1, 1.3, 1],
                  opacity: [0.7, 1, 0.7]
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity
                }}
              >
                <Sparkles className="w-4 h-4 text-[#f9d58f]" />
              </motion.div>
            </div>
          </motion.button>
        </div>

        {/* Hidden Meaning Reveal */}
        <AnimatePresence>
          {isRevealed && (
            <motion.div
              initial={{ opacity: 0, height: 0, scale: 0.9 }}
              animate={{ opacity: 1, height: 'auto', scale: 1 }}
              exit={{ opacity: 0, height: 0, scale: 0.9 }}
              transition={{ duration: 0.4, type: 'spring' }}
              className="overflow-hidden mt-4"
            >
              <div className="bg-gradient-to-br from-[#fff9e6] to-[#ffd5b8]/30 rounded-[1.5rem] p-5 border-2 border-[#f9d58f]/30 shadow-inner">
                <div className="flex items-start gap-2">
                  <span className="text-2xl">🎁</span>
                  <div>
                    <h4 className="text-[#4a4063] font-bold mb-2 flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-[#f9d58f]" />
                      The Secret Behind the Joke
                    </h4>
                    <p className="text-[#6b5a7d] leading-relaxed text-sm">
                      {joke.hiddenMeaning}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}

function AIAvatar() {
  return (
    <motion.div
      className="relative w-16 h-16 flex-shrink-0"
      animate={{
        y: [0, -8, 0],
      }}
      transition={{
        duration: 3,
        repeat: Infinity,
        ease: 'easeInOut'
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-[#ffc0e3] via-[#e0c3fc] to-[#c3dbf7] rounded-full blur-md opacity-60 animate-pulse" />
      <div className="relative w-full h-full bg-gradient-to-br from-[#ffc0e3] to-[#e0c3fc] rounded-full flex items-center justify-center text-3xl shadow-lg border-2 border-white">
        🎭
      </div>
      <motion.div
        className="absolute -top-1 -right-1"
        animate={{ rotate: [0, 15, -15, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <Sparkles className="w-5 h-5 text-[#f9d58f]" />
      </motion.div>
    </motion.div>
  );
}

export default function App() {
  const [messages, setMessages] = useState<Joke[]>(sampleJokes);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const topic = inputValue.trim();
    setInputValue('');
    setError(null);
    setIsLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await fetch(`${apiUrl}/api/joke`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || `Server error (${response.status})`);
      }

      const data = await response.json();
      const newJoke: Joke = {
        id: messages.length + 1,
        text: data.joke,
        emoji: '🎬',
        hiddenMeaning: data.hidden_meaning,
      };
      setMessages((prev) => [...prev, newJoke]);
    } catch (err: any) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative w-full min-h-screen overflow-hidden bg-gradient-to-br from-[#fef5ff] via-[#fce7f3] to-[#e0e7ff]">
      {/* Floating Decorations */}
      {[...Array(8)].map((_, i) => (
        <FloatingDecoration
          key={`bubble-${i}`}
          type="bubble"
          delay={i * 2}
        />
      ))}
      {[...Array(6)].map((_, i) => (
        <FloatingDecoration
          key={`star-${i}`}
          type="star"
          delay={i * 3}
        />
      ))}
      {[...Array(4)].map((_, i) => (
        <FloatingDecoration
          key={`heart-${i}`}
          type="heart"
          delay={i * 4}
        />
      ))}
      {[...Array(5)].map((_, i) => (
        <FloatingDecoration
          key={`sparkle-${i}`}
          type="sparkle"
          delay={i * 2.5}
        />
      ))}

      {/* Main Chat Container */}
      <div className="relative z-10 max-w-4xl mx-auto px-4 py-8 min-h-screen flex flex-col">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center gap-4 mb-3">
            <AIAvatar />
          </div>
          <h1 className="font-['Fredoka'] text-4xl md:text-5xl mb-2 bg-gradient-to-r from-[#a78bfa] via-[#ffc0e3] to-[#c3dbf7] bg-clip-text text-transparent">
            Bollywood Comedy AI 🎬
          </h1>
          <p className="text-[#9ca3af] font-medium">
            Your dreamy pastel cinema universe of desi chaos ✨
          </p>
        </motion.div>

        {/* Chat Messages */}
        <div className="flex-1 mb-6 space-y-4">
          {messages.length === 0 && !isLoading ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 }}
              className="text-center py-20"
            >
              <div className="text-6xl mb-4">🎭</div>
              <h2 className="text-2xl font-['Fredoka'] text-[#a78bfa] mb-2">
                Namaste! Ready for some Bollywood chaos?
              </h2>
              <p className="text-[#9ca3af]">
                Enter any topic below and watch the filmy magic unfold! ✨
              </p>
            </motion.div>
          ) : (
            <>
              {messages.map((joke) => (
                <div key={joke.id} className="flex gap-4 items-start">
                  <div className="hidden sm:block">
                    <div className="w-12 h-12 bg-gradient-to-br from-[#e0c3fc] to-[#c3dbf7] rounded-full flex items-center justify-center text-2xl shadow-md">
                      🤖
                    </div>
                  </div>
                  <div className="flex-1">
                    <JokeCard joke={joke} />
                  </div>
                </div>
              ))}

              {/* Loading Indicator */}
              <AnimatePresence>
                {isLoading && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="flex gap-4 items-start"
                  >
                    <div className="hidden sm:block">
                      <div className="w-12 h-12 bg-gradient-to-br from-[#e0c3fc] to-[#c3dbf7] rounded-full flex items-center justify-center text-2xl shadow-md">
                        🤖
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="bg-gradient-to-br from-[#ffc0e3]/20 via-[#e0c3fc]/20 to-[#c3dbf7]/20 backdrop-blur-sm rounded-[2rem] p-6 shadow-lg border-2 border-white/40">
                        <div className="flex items-center gap-3">
                          <Loader2 className="w-6 h-6 text-[#a78bfa] animate-spin" />
                          <p className="text-[#4a4063] font-medium animate-pulse">
                            Cooking up a Bollywood joke... 🎬✨
                          </p>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Error Message */}
              <AnimatePresence>
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="flex gap-4 items-start"
                  >
                    <div className="hidden sm:block">
                      <div className="w-12 h-12 bg-gradient-to-br from-[#ffc0e3] to-[#f87171] rounded-full flex items-center justify-center text-2xl shadow-md">
                        😵
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="bg-gradient-to-br from-[#fef2f2] to-[#ffd5b8]/30 rounded-[2rem] p-6 shadow-lg border-2 border-red-200/40">
                        <p className="text-[#4a4063] font-medium">{error}</p>
                        <button
                          onClick={() => setError(null)}
                          className="mt-2 text-sm text-[#a78bfa] hover:underline cursor-pointer"
                        >
                          Dismiss
                        </button>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </>
          )}
        </div>

        {/* Input Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="sticky bottom-0 pb-6"
        >
          <div className="bg-white/80 backdrop-blur-md rounded-full shadow-2xl border-2 border-[#e0c3fc]/30 p-2 flex items-center gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder={isLoading ? "Generating joke..." : "Enter a topic for Bollywood chaos ✨"}
              disabled={isLoading}
              className={`flex-1 bg-transparent px-6 py-3 outline-none text-[#4a4063] placeholder:text-[#c4b5fd] ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            />
            <motion.button
              onClick={handleSend}
              whileHover={isLoading ? {} : { scale: 1.05 }}
              whileTap={isLoading ? {} : { scale: 0.95 }}
              disabled={isLoading}
              className={`bg-gradient-to-r from-[#a78bfa] to-[#ffc0e3] text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 group ${isLoading ? 'opacity-60 cursor-not-allowed' : ''}`}
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              )}
            </motion.button>
          </div>

          {/* Cute decorative elements around input */}
          <div className="flex justify-center gap-3 mt-3 text-2xl">
            <motion.span
              animate={{ y: [0, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0 }}
            >
              ✨
            </motion.span>
            <motion.span
              animate={{ y: [0, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.3 }}
            >
              🎭
            </motion.span>
            <motion.span
              animate={{ y: [0, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.6 }}
            >
              💫
            </motion.span>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
