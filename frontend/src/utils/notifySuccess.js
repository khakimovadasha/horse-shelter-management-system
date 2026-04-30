import { Notify } from 'quasar'

export const notifySuccess = (message) => {
  Notify.create({
    message,
    icon: 'check',
    position: 'top-right',
    timeout: 2500,
    progress: false,
    group: false,
    classes: 'app-success-notify',
  })
}
