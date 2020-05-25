<template>
  <v-app>
    <!-- <v-app-bar
      app
      color="primary"
      dark
    ></v-app-bar> -->
    <Home></Home>
  </v-app>
</template>

<script>
import Home from '@/components/Home'
export default {
  name: 'App',

  components: {
    'Home': Home
  },

  data: () => ({
    //
  })
}
</script>
