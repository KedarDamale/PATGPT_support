import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, Trash2, Pencil } from "lucide-react";

type SidebarCellProps = {
    id: number;
    title: string;
    isActive?: boolean;
    onClick?: () => void;
    onDelete?: (id: number) => void;
    onRename?: (id: number, newTitle: string) => void;
};

export default function SidebarCell({
    id,
    title,
    isActive = false,
    onClick,
    onDelete,
    onRename,
}: SidebarCellProps) {
    const [isHovered, setIsHovered] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [editValue, setEditValue] = useState(title);

    const handleRename = () => {
        if (editValue.trim()) {
            onRename?.(id, editValue.trim());
        } else {
            setEditValue(title);
        }
        setIsEditing(false);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") handleRename();
        if (e.key === "Escape") {
            setEditValue(title);
            setIsEditing(false);
        }
    };

    return (
        <motion.div
            onHoverStart={() => setIsHovered(true)}
            onHoverEnd={() => setIsHovered(false)}
            onClick={() => !isEditing && onClick?.()}
            whileTap={{ scale: 0.98 }}
            className="group relative flex items-center gap-2.5 px-3 py-2 rounded-xl cursor-pointer transition-all duration-150"
            style={{
                background: isActive
                    ? "rgba(255,255,255,0.08)"
                    : isHovered
                        ? "rgba(255,255,255,0.04)"
                        : "transparent",
                border: isActive
                    ? "1px solid rgba(255,255,255,0.1)"
                    : "1px solid transparent",
            }}
        >
            {/* Icon */}
            <MessageSquare
                className="shrink-0"
                style={{
                    width: "13px",
                    height: "13px",
                    color: isActive
                        ? "rgba(255,255,255,0.6)"
                        : "rgba(255,255,255,0.25)",
                }}
            />

            {/* Title or edit input */}
            {isEditing ? (
                <input
                    autoFocus
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                    onBlur={handleRename}
                    onKeyDown={handleKeyDown}
                    onClick={(e) => e.stopPropagation()}
                    className="flex-1 bg-transparent outline-none text-xs min-w-0"
                    style={{
                        color: "rgba(255,255,255,0.85)",
                        caretColor: "rgba(255,255,255,0.7)",
                        borderBottom: "1px solid rgba(255,255,255,0.2)",
                    }}
                />
            ) : (
                <span
                    className="flex-1 text-xs truncate"
                    style={{
                        color: isActive
                            ? "rgba(255,255,255,0.85)"
                            : "rgba(255,255,255,0.45)",
                    }}
                >
                    {title}
                </span>
            )}

            {/* Action buttons */}
            <AnimatePresence>
                {isHovered && !isEditing && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.1 }}
                        className="flex items-center gap-0.5 shrink-0"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <motion.button
                            whileHover={{ scale: 1.15 }}
                            whileTap={{ scale: 0.9 }}
                            onClick={() => setIsEditing(true)}
                            className="w-6 h-6 flex items-center justify-center rounded-md cursor-pointer"
                            style={{ color: "rgba(255,255,255,0.3)" }}
                            onMouseEnter={(e) =>
                            ((e.currentTarget as HTMLElement).style.color =
                                "rgba(255,255,255,0.7)")
                            }
                            onMouseLeave={(e) =>
                            ((e.currentTarget as HTMLElement).style.color =
                                "rgba(255,255,255,0.3)")
                            }
                        >
                            <Pencil size={11} />
                        </motion.button>
                        <motion.button
                            whileHover={{ scale: 1.15 }}
                            whileTap={{ scale: 0.9 }}
                            onClick={() => onDelete?.(id)}
                            className="w-6 h-6 flex items-center justify-center rounded-md cursor-pointer"
                            style={{ color: "rgba(255,255,255,0.3)" }}
                            onMouseEnter={(e) =>
                            ((e.currentTarget as HTMLElement).style.color =
                                "rgba(239,68,68,0.8)")
                            }
                            onMouseLeave={(e) =>
                            ((e.currentTarget as HTMLElement).style.color =
                                "rgba(255,255,255,0.3)")
                            }
                        >
                            <Trash2 size={11} />
                        </motion.button>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}