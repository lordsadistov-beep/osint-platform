interface User {
  username: string
  avatar_url?: string
  level?: number
}

export function UserAvatar({ user }: { user: User }) {
  return (
    <div className="flex items-center gap-2">
      {user.avatar_url ? (
        <img src={user.avatar_url} alt="" className="h-7 w-7 rounded-full" />
      ) : (
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary-600 text-xs font-bold">
          {user.username[0].toUpperCase()}
        </div>
      )}
      <span className="text-sm text-gray-300">{user.username}</span>
      {user.level && (
        <span className="text-xs text-gray-500">Lv.{user.level}</span>
      )}
    </div>
  )
}
