<template>
  <!-- PART 4: Add your code here -->
  <div>
    <p>{{ name }}</p>
    <Counter :episodes = 'episodes_seen'></Counter>
  </div>
</template>

<script>
// PART 4: Add your code here
import Counter from "./Counter.vue";
export default {
  name: "show",
  components: {Counter},
  props: {
    key : Number,
    id: Number,
    name: String,
    episodes_seen: Number
  }
};
</script>

<style>
</style>
