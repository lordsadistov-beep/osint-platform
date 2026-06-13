import { ToolWidget } from '../components/ToolWidget'

export function ToolEmail() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Email Checker</h1>
      <p className="mb-4 text-sm text-gray-500">Проверка email: репутация, утечки, сервисы</p>
      <ToolWidget toolSlug="email" />
    </div>
  )
}
