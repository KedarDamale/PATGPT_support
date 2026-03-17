import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

type AiMessageCardProps = {
  message: string;
  timestamp?: string;
  isLoading?: boolean;
};

export default function AiMessageCard({
  message,
  timestamp,
  isLoading = false,
}: AiMessageCardProps) {
  const time =
    timestamp ??
    new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  return (
    <motion.div
      initial={{ opacity: 0, y: 10, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="flex justify-start w-full px-3 sm:px-4 md:px-6"
    >
      <div className="flex items-start gap-2 sm:gap-3 max-w-[85%] sm:max-w-[75%] md:max-w-[65%]">

        {/* Avatar */}
        <div
          className="shrink-0 flex items-center justify-center rounded-xl mt-0.5"
          style={{
            width: "clamp(28px, 3.5vw, 34px)",
            height: "clamp(28px, 3.5vw, 34px)",
            background: "rgba(255,255,255,0.06)",
            border: "1px solid rgba(255,255,255,0.12)",
          }}
        >
          <Sparkles
            style={{
              width: "clamp(11px, 1.4vw, 14px)",
              height: "clamp(11px, 1.4vw, 14px)",
              color: "rgba(255,255,255,0.6)",
            }}
          />
        </div>

        <div className="flex flex-col items-start gap-1">

          {/* Bubble */}
          <div
            className="px-4 py-3 rounded-2xl rounded-tl-sm"
            style={{
              background: "rgba(255,255,255,0.04)",
              border: "1px solid rgba(255,255,255,0.08)",
              backdropFilter: "blur(16px)",
              WebkitBackdropFilter: "blur(16px)",
              boxShadow: "0 4px 24px rgba(0,0,0,0.15)",
            }}
          >
            {isLoading ? (
              /* Typing dots */
              <div className="flex items-center gap-1.5 py-1 px-1">
                {[0, 1, 2].map((i) => (
                  <motion.span
                    key={i}
                    className="rounded-full"
                    style={{
                      width: "6px",
                      height: "6px",
                      background: "rgba(255,255,255,0.4)",
                    }}
                    animate={{ y: [0, -5, 0], opacity: [0.4, 1, 0.4] }}
                    transition={{
                      duration: 1,
                      repeat: Infinity,
                      delay: i * 0.18,
                      ease: "easeInOut",
                    }}
                  />
                ))}
              </div>
            ) : (
              <p
                className="leading-relaxed whitespace-pre-wrap wrap-break-words"
                style={{
                  color: "rgba(255,255,255,0.78)",
                  fontSize: "clamp(13px, 1.6vw, 15px)",
                }}
              >
                {message}
              </p>
            )}
          </div>

          {/* Timestamp */}
          {!isLoading && (
            <span
              style={{
                color: "rgba(255,255,255,0.22)",
                fontSize: "10px",
                paddingLeft: "4px",
              }}
            >
              AskPat · {time}
            </span>
          )}

        </div>
      </div>
    </motion.div>
  );
}