const { createVuetify } = Vuetify;
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'timeLight',
    themes: {
      timeLight: {
        colors: {
          ligth: '#EBEBEB',
          primary: '#FF6700',
          secondary: '#004E98',
          border: '#C0C0C0',
          text: '#000000',
          title: '#3A6EA5',
          error: '#e63946',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
        },
      },
    },
  },
});
