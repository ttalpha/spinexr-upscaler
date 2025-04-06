import { useEffect, useState } from 'react'
import uniqid from 'uniqid'

export const useAnonUserId = () => {
  const [userId, setUserId] = useState<string | null>(null)

  useEffect(() => {
    let savedUserId = localStorage.getItem('userId')
    if (!savedUserId) savedUserId = uniqid()
    setUserId(savedUserId)
  }, [])

  useEffect(() => {
    if (userId) localStorage.setItem('userId', userId)
  }, [userId])

  return { userId }
}
