import { Card } from './common/Card'
import { Badge } from './common/Badge'

export function SearchResult({ data, tool }: { data: any; tool: string }) {
  if (tool === 'username') {
    return (
      <div className="space-y-2">
        <p className="text-xs text-gray-500">
          Проверено сайтов: {data.sites_checked} | Найдено: {data.found.length} | {data.elapsed_ms}ms
        </p>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {data.found.map((site: any, i: number) => (
            <a
              key={i}
              href={site.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 rounded-lg border border-gray-800 bg-gray-900/50 p-2 text-sm hover:border-primary-600"
            >
              <div className="flex h-8 w-8 items-center justify-center rounded bg-gray-800 text-xs font-bold uppercase">
                {site.site[0]}
              </div>
              <div>
                <p className="text-gray-200">{site.site}</p>
                <p className="text-xs text-gray-500 truncate max-w-[200px]">{site.url}</p>
              </div>
            </a>
          ))}
        </div>
      </div>
    )
  }

  if (tool === 'email') {
    return (
      <div className="space-y-2 text-sm">
        <p>Email: <span className="text-gray-300">{data.email}</span></p>
        {data.gravatar && (
          <img src={data.gravatar} alt="gravatar" className="h-10 w-10 rounded-full" />
        )}
        {data.breaches.length > 0 && (
          <div>
            <p className="text-red-400">Утечки: {data.breaches.length}</p>
            <ul className="list-inside list-disc text-xs text-gray-400">
              {data.breaches.map((b: string, i: number) => <li key={i}>{b}</li>)}
            </ul>
          </div>
        )}
        {data.domain_info && (
          <p>Domain: <span className="text-gray-300">{data.domain_info.domain}</span></p>
        )}
      </div>
    )
  }

  if (tool === 'phone') {
    return (
      <div className="space-y-2 text-sm">
        <p>Номер: <span className="text-gray-300">{data.phone}</span></p>
        <p>Страна: {data.country}</p>
        <p>Оператор: {data.carrier}</p>
        <div>
          <p>Мессенджеры:</p>
          <div className="flex gap-2 mt-1">
            {Object.entries(data.messengers).map(([name, active]) => (
              <Badge key={name} variant={active ? 'success' : 'default'}>{name}</Badge>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (tool === 'domain') {
    return (
      <div className="space-y-2 text-sm">
        <p>Domain: <span className="text-gray-300">{data.domain}</span></p>
        {data.ip && <p>IP: <span className="text-gray-300">{data.ip}</span></p>}
        {data.dns?.a && (
          <p>A записи: <span className="text-gray-300">{data.dns.a.join(', ')}</span></p>
        )}
        {data.subdomains.length > 0 && (
          <div>
            <p>Поддомены ({data.subdomains.length}):</p>
            <ul className="list-inside list-disc text-xs text-gray-400">
              {data.subdomains.map((s: string, i: number) => <li key={i}>{s}</li>)}
            </ul>
          </div>
        )}
      </div>
    )
  }

  if (tool === 'leaks') {
    return (
      <div className="space-y-2">
        <p className="text-sm">
          {data.found ? `Найдено: ${data.entries.length}` : 'Ничего не найдено'}
        </p>
        {data.entries.length > 0 && (
          <div className="max-h-60 overflow-y-auto space-y-1">
            {data.entries.map((e: any, i: number) => (
              <Card key={i} className="p-2 text-xs">
                <p>{e.email || e.username || e.phone}</p>
                {e.password_plain && <p className="text-yellow-400">Pass: {e.password_plain}</p>}
                <p className="text-gray-500">Source: {e.source}</p>
              </Card>
            ))}
          </div>
        )}
      </div>
    )
  }

  if (tool === 'metadata') {
    return (
      <div className="space-y-2 text-sm">
        <p>Файл: <span className="text-gray-300">{data.filename}</span></p>
        <p>Тип: {data.type}</p>
        <p>Размер: {(data.size / 1024).toFixed(1)} KB</p>
        {data.camera && <p>Камера: {data.camera}</p>}
        {data.created_date && <p>Дата: {data.created_date}</p>}
        {data.gps && <p className="text-green-400">GPS данные найдены</p>}
        {Object.keys(data.exif).length > 0 && (
          <details>
            <summary className="cursor-pointer text-primary-400">EXIF ({Object.keys(data.exif).length})</summary>
            <pre className="mt-1 max-h-40 overflow-y-auto text-xs text-gray-400">
              {JSON.stringify(data.exif, null, 2)}
            </pre>
          </details>
        )}
      </div>
    )
  }

  return <pre className="text-xs text-gray-400">{JSON.stringify(data, null, 2)}</pre>
}
