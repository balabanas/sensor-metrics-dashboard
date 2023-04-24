<template>

  <div>
    <dashboard :filterPattern="query">
    </dashboard>
  </div>

</template>


<script>
import Dashboard from '../components/Dashboard.vue'

export default {
  components: {
    Dashboard,
  },
  props: {
    query: String
  },
}
</script>
