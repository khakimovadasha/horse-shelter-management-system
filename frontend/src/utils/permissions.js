export const isAdmin = (user) => user?.role === 'admin'

export const isVeterinarian = (user) => user?.role === 'veterinarian'

export const canCreateHorse = (user) => isAdmin(user)

export const canEditHorse = (user) => {
  return isAdmin(user) || isVeterinarian(user)
}

export const canCreateMedicalRecord = (user) => {
  return isAdmin(user) || isVeterinarian(user)
}

export const canCreateProcedure = (user) => {
  return isAdmin(user) || isVeterinarian(user)
}

export const canCompleteProcedure = (user) => {
  return isAdmin(user) || isVeterinarian(user)
}

export const canCreateTask = (user) => isAdmin(user)
