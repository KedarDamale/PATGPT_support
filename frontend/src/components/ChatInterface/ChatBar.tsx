import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import TextareaAutosize from "react-textarea-autosize";
import { Send, X } from "lucide-react";

type ChatBarProps = {
  onSend?: (message: string) => void;
};

const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

export default function ChatBar({ onSend }: ChatBarProps) {
  const [input, setInput] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (!input.trim()) return;
    onSend?.(input.trim());
    setInput("");
    textareaRef.current?.focus();
  };

  const handleKey = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (isMobile) return;
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClear = () => {
    setInput("");
    textareaRef.current?.focus();
  };

  return (
    <div className="w-full max-w-3xl mx-auto px-3 sm:px-4 md:px-6 flex flex-col gap-2">

      {/* Input bar */}
      <motion.div
        animate={{
          boxShadow: isFocused
            ? "0 0 0 1.5px rgba(255,255,255,0.35), 0 8px 40px rgba(0,0,0,0.5), 0 0 32px rgba(255,255,255,0.06)"
            : "0 4px 24px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.04)",
          borderColor: isFocused
            ? "rgba(255,255,255,0.35)"
            : "rgba(255,255,255,0.12)",
        }}
        transition={{ duration: 0.25 }}
        className="flex items-center w-full rounded-2xl sm:rounded-3xl"
        style={{
          background: "rgba(255,255,255,0.05)",
          border: "1px solid rgba(255,255,255,0.12)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          padding: "clamp(10px, 2vw, 16px) clamp(12px, 2.5vw, 20px)",
          gap: "clamp(8px, 1.5vw, 14px)",
        }}
      >

        {/* Textarea */}
        <TextareaAutosize
          ref={textareaRef}
          minRows={1}
          maxRows={6}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder="Got a problem? Ask Pat..."
          className="flex-1 bg-transparent outline-none resize-none leading-relaxed placeholder:opacity-40"
          style={{
            color: "rgba(255,255,255,0.9)",
            caretColor: "rgba(255,255,255,0.9)",
            scrollbarWidth: "none",
            fontSize: "clamp(14px, 1.8vw, 16px)",
            paddingTop: "2px",
            paddingBottom: "2px",
          }}
        />

        {/* Buttons */}
        <div
          className="flex items-center shrink-0"
          style={{ gap: "clamp(4px, 1vw, 8px)", marginBottom: "1px" }}
        >

          {/* Clear button */}
          <AnimatePresence>
            {input.trim() && (
              <motion.button
                initial={{ opacity: 0, scale: 0.6 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.6 }}
                transition={{ duration: 0.15 }}
                onClick={handleClear}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="flex items-center justify-center rounded-lg cursor-pointer"
                style={{
                  color: "rgba(255,255,255,0.3)",
                  width: "clamp(28px, 3.5vw, 36px)",
                  height: "clamp(28px, 3.5vw, 36px)",
                  background: "rgba(255,255,255,0.05)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
                onMouseEnter={(e) =>
                  ((e.currentTarget as HTMLButtonElement).style.color =
                    "rgba(255,255,255,0.65)")
                }
                onMouseLeave={(e) =>
                  ((e.currentTarget as HTMLButtonElement).style.color =
                    "rgba(255,255,255,0.3)")
                }
              >
                <X
                  style={{
                    width: "clamp(13px, 1.6vw, 17px)",
                    height: "clamp(13px, 1.6vw, 17px)",
                  }}
                />
              </motion.button>
            )}
          </AnimatePresence>

          {/* Send button */}
          <motion.button
            onClick={handleSend}
            disabled={!input.trim()}
            whileHover={input.trim() ? { scale: 1.08 } : {}}
            whileTap={input.trim() ? { scale: 0.88 } : {}}
            transition={{ duration: 0.15 }}
            className="flex items-center justify-center rounded-xl cursor-pointer disabled:opacity-20 disabled:cursor-not-allowed"
            style={{
              background: input.trim()
                ? "rgba(255,255,255,0.18)"
                : "transparent",
              border: "1px solid rgba(255,255,255,0.25)",
              width: "clamp(34px, 4vw, 44px)",
              height: "clamp(34px, 4vw, 44px)",
              transition: "background 0.2s",
            }}
          >
            <Send
              color="rgba(255,255,255,0.85)"
              style={{
                width: "clamp(13px, 1.6vw, 17px)",
                height: "clamp(13px, 1.6vw, 17px)",
              }}
            />
          </motion.button>
        </div>
      </motion.div>

      {/* Keyboard hint — desktop only, shows on focus */}
      <AnimatePresence>
        {isFocused && !isMobile && (
          <motion.p
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.4 }}
            className="text-center hidden sm:block"
            style={{ color: "rgba(255,255,255,0.5)", fontSize: "12px" }}
          >
            <kbd
              style={{
                padding: "1px 5px",
                borderRadius: "4px",
                border: "1px solid rgba(255,255,255,0.15)",
                color: "rgba(255,255,255,0.5)",
                fontSize: "10px",
              }}
            >
              Enter
            </kbd>{" "}
            to send &nbsp;·&nbsp;{" "}
            <kbd
              style={{
                padding: "1px 5px",
                borderRadius: "4px",
                border: "1px solid rgba(255,255,255,0.15)",
                color: "rgba(255,255,255,0.5)",
                fontSize: "10px",
              }}
            >
              Shift + Enter
            </kbd>{" "}
            for new line
          </motion.p>
        )}
      </AnimatePresence>

    </div>
  );
}