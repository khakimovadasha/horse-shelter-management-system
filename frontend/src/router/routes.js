const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('pages/DashboardPage.vue'),
      },
      {
        path: 'horses',
        name: 'horses',
        component: () => import('pages/HorsesPage.vue'),
      },
      {
        path: 'procedures',
        name: 'procedures',
        component: () => import('pages/ProceduresPage.vue'),
      },
      {
        path: 'tasks',
        name: 'tasks',
        component: () => import('pages/TasksPage.vue'),
      },
      {
        path: 'calendar',
        name: 'calendar',
        component: () => import('pages/CalendarPage.vue'),
      },
      {
        path: 'finances',
        name: 'finances',
        component: () => import('pages/FinancesPage.vue'),
      },
      {
        path: 'reports',
        name: 'reports',
        component: () => import('pages/ReportsPage.vue'),
      },
      {
        path: 'users',
        name: 'users',
        component: () => import('pages/UsersPage.vue'),
      },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes