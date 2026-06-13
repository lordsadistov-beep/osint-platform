import { cn } from '../lib/utils'

export function ProgressBar({ value, max = 100, className }: { value: number; max?: number; className?: string }) {
  const pct = Math.min((value / max) * 100, 100)
  return (
    <div className={cn('h-2 w-full rounded-full bg-gray-800', className)}>
      <div
        className="h-full rounded-full bg-primary-500 transition-all duration-300"
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}
