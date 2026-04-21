const routes = [
  {
    path: '/',
    component: () => import('layouts/PublicLayout/PublicLayout.vue'),
    children: [
      {
        path: '',
        name: 'landing',
        component: () => import('pages/LandingPage/LandingPage.vue'),
      },
    ],
  },

  {
    path: '/app',
    component: () => import('layouts/MainLayout/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('pages/DashboardPage/DashboardPage.vue'),
      },
      {
        path: 'horses',
        name: 'horses',
        component: () => import('pages/HorsesPage/HorsesPage.vue'),
      },
      {
        path: 'horses/:id',
        name: 'horse',
        component: () => import('pages/HorsePage/HorsePage.vue'),
      },
      {
        path: 'procedures',
        name: 'procedures',
        component: () => import('pages/ProceduresPage/ProceduresPage.vue'),
      },
      {
        path: 'tasks',
        name: 'tasks',
        component: () => import('pages/TasksPage/TasksPage.vue'),
      },
      {
        path: 'calendar',
        name: 'calendar',
        component: () => import('pages/CalendarPage/CalendarPage.vue'),
      },
      {
        path: 'finances',
        name: 'finances',
        component: () => import('pages/FinancesPage/FinancesPage.vue'),
      },
      {
        path: 'reports',
        name: 'reports',
        component: () => import('pages/ReportsPage/ReportsPage.vue'),
      },
      {
        path: 'users',
        name: 'users',
        component: () => import('pages/UsersPage/UsersPage.vue'),
      },
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound/ErrorNotFound.vue'),
  },
]

export default routes