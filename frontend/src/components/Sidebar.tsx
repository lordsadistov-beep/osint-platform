import { Link, useLocation } from 'react-router-dom'
import { cn } from '../lib/utils'
import { useUiStore } from '../stores/uiStore'

const links = [
  { to: '/learn', label: 'Уроки', icon: '📚' },
  { to: '/challenges', label: 'Челленджи', icon: '🏆' },
  { to: '/tools/username', label: 'Username Search', icon: '🔍' },
  { to: '/tools/email', label: 'Email Checker', icon: '📧' },
  { to: '/tools/phone', label: 'Phone Checker', icon: '📱' },
  { to: '/tools/domain', label: 'Domain Lookup', icon: '🌐' },
  { to: '/tools/leaks', label: 'Leak Search', icon: '💀' },
  { to: '/tools/metadata', label: 'Metadata', icon: '🖼️' },
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/dashboard/graph', label: 'Graph', icon: '🔗' },
]

export function Sidebar() {
  const location = useLocation()
  const { sidebarOpen } = useUiStore()

  if (!sidebarOpen) return null

  return (
    <aside className="fixed left-0 top-14 h-[calc(100vh-3.5rem)] w-56 overflow-y-auto border-r border-gray-800 bg-gray-950 p-2">
      <nav className="space-y-1">
        {links.map((link) => (
          <Link
            key={link.to}
            to={link.to}
            className={cn(
              'flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors',
              location.pathname === link.to
                ? 'bg-primary-600/20 text-primary-400'
                : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'
            )}
          >
            <span>{link.icon}</span>
            {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  )
}
