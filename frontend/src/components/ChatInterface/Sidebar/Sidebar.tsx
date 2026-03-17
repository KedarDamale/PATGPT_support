import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  SquarePen,
  ExternalLink,
  Settings,
  User,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import SidebarCell from "./SidebarCell";

type Chat = {
  id: number;
  title: string;
};

type SidebarProps = {
  chats?: Chat[];
  activeChatId?: number;
  onNewChat?: () => void;
  onSelectChat?: (id: number) => void;
  onDeleteChat?: (id: number) => void;
  onRenameChat?: (id: number, newTitle: string) => void;
  onSettings?: () => void;
  onAccount?: () => void;
};

const SIDEBAR_WIDTH = 260;

export default function Sidebar({
  chats = [],
  activeChatId,
  onNewChat,
  onSelectChat,
  onDeleteChat,
  onRenameChat,
  onSettings,
  onAccount,
}: SidebarProps) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <>
      {/* Sidebar panel */}
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.aside
            key="sidebar"
            initial={{ x: -SIDEBAR_WIDTH, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -SIDEBAR_WIDTH, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="fixed top-0 left-0 h-screen z-40 flex flex-col"
            style={{
              width: SIDEBAR_WIDTH,
              background: "rgba(10,10,10,0.85)",
              borderRight: "1px solid rgba(255,255,255,0.07)",
              backdropFilter: "blur(24px)",
              WebkitBackdropFilter: "blur(24px)",
              boxShadow: "4px 0 32px rgba(0,0,0,0.5)",
            }}
          >
            {/* Top — Logo + New Chat */}
            <div className="flex flex-col gap-2 px-3 pt-5 pb-3">

              {/* PATGPT branding */}
              <a
                href="https://patgpt.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-2 py-1.5 rounded-xl group"
                style={{ textDecoration: "none" }}
              >
                <div
                  className="w-7 h-7 rounded-lg flex items-center justify-center shrink-0"
                  style={{
                    background: "rgba(255,255,255,0.08)",
                    border: "1px solid rgba(255,255,255,0.12)",
                  }}
                >
                  <span style={{ fontSize: "13px" }}>✦</span>
                </div>
                <span
                  className="font-semibold tracking-wide text-sm"
                  style={{ color: "rgba(255,255,255,0.75)" }}
                >
                  PATGPT
                </span>
                <ExternalLink
                  size={11}
                  className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity"
                  style={{ color: "rgba(255,255,255,0.3)" }}
                />
              </a>

              {/* Divider */}
              <div style={{ height: "1px", background: "rgba(255,255,255,0.06)" }} />

              {/* New Chat */}
              <motion.button
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.98 }}
                onClick={onNewChat}
                className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl cursor-pointer w-full"
                style={{
                  background: "rgba(255,255,255,0.06)",
                  border: "1px solid rgba(255,255,255,0.1)",
                  color: "rgba(255,255,255,0.75)",
                }}
              >
                <SquarePen size={14} />
                <span className="text-sm font-medium">New Chat</span>
              </motion.button>
            </div>

            {/* Recent chats */}
            <div className="flex flex-col flex-1 overflow-hidden px-3">
              <p
                className="text-xs font-semibold uppercase tracking-widest px-2 mb-2"
                style={{ color: "rgba(255,255,255,0.2)" }}
              >
                Recent
              </p>

              <div
                className="flex-1 overflow-y-auto flex flex-col gap-0.5 pr-0.5"
                style={{ scrollbarWidth: "none" }}
              >
                <AnimatePresence initial={false}>
                  {chats.length === 0 ? (
                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="text-xs px-3 py-4 text-center"
                      style={{ color: "rgba(255,255,255,0.18)" }}
                    >
                      No recent chats yet
                    </motion.p>
                  ) : (
                    chats.map((chat, i) => (
                      <motion.div
                        key={chat.id}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -10 }}
                        transition={{ duration: 0.18, delay: i * 0.03 }}
                      >
                        <SidebarCell
                          id={chat.id}
                          title={chat.title}
                          isActive={chat.id === activeChatId}
                          onClick={() => onSelectChat?.(chat.id)}
                          onDelete={onDeleteChat}
                          onRename={onRenameChat}
                        />
                      </motion.div>
                    ))
                  )}
                </AnimatePresence>
              </div>
            </div>

            {/* Bottom — Account + Settings */}
            <div
              className="flex flex-col gap-1 px-3 py-4"
              style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}
            >
              <motion.button
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.97 }}
                onClick={onAccount}
                className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl cursor-pointer w-full"
                style={{ color: "rgba(255,255,255,0.45)" }}
                onMouseEnter={(e) =>
                  ((e.currentTarget as HTMLElement).style.background =
                    "rgba(255,255,255,0.04)")
                }
                onMouseLeave={(e) =>
                  ((e.currentTarget as HTMLElement).style.background = "transparent")
                }
              >
                <div
                  className="w-6 h-6 rounded-full flex items-center justify-center shrink-0"
                  style={{
                    background: "rgba(255,255,255,0.08)",
                    border: "1px solid rgba(255,255,255,0.1)",
                  }}
                >
                  <User size={12} style={{ color: "rgba(255,255,255,0.5)" }} />
                </div>
                <span className="text-xs truncate">My Account</span>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.97 }}
                onClick={onSettings}
                className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl cursor-pointer w-full"
                style={{ color: "rgba(255,255,255,0.45)" }}
                onMouseEnter={(e) =>
                  ((e.currentTarget as HTMLElement).style.background =
                    "rgba(255,255,255,0.04)")
                }
                onMouseLeave={(e) =>
                  ((e.currentTarget as HTMLElement).style.background = "transparent")
                }
              >
                <Settings size={14} />
                <span className="text-xs">Settings</span>
              </motion.button>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Toggle button */}
      <motion.button
        onClick={() => setIsOpen((o) => !o)}
        animate={{ left: isOpen ? SIDEBAR_WIDTH - 12 : 8 }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
        className="fixed top-5 z-50 w-6 h-6 rounded-full flex items-center justify-center cursor-pointer"
        style={{
          background: "rgba(255,255,255,0.08)",
          border: "1px solid rgba(255,255,255,0.12)",
          color: "rgba(255,255,255,0.5)",
        }}
        whileHover={{ scale: 1.1, background: "rgba(255,255,255,0.14)" }}
        whileTap={{ scale: 0.9 }}
      >
        {isOpen ? <ChevronLeft size={12} /> : <ChevronRight size={12} />}
      </motion.button>
    </>
  );
}