import { ToolWidget } from '../components/ToolWidget'

export function ToolUsername() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Username Search</h1>
      <p className="mb-4 text-sm text-gray-500">Поиск аккаунтов по username в 300+ сервисах</p>
      <ToolWidget toolSlug="username" />
    </div>
  )
}
