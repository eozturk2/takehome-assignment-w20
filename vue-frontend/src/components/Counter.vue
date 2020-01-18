<template>
  <div>
    <button v-on:click="count++">+1 Episode</button>
    <button v-on:click="count--">-1 Episode</button>
    <p>{{ count }}</p>
  </div>
</template>

<script>
export default {
  props: {
     episodes: Number,
  },
  data() {
    return {
      count: 0
    };
  }
};
</script>

<style>
</style>

