import { cn } from '../../lib/utils'

export function Card({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('rounded-xl border border-gray-800 bg-gray-900 p-4', className)}
      {...props}
    >
      {children}
    </div>
  )
}
