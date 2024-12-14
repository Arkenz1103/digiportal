<template>
  <div
    class="relative w-32 h-32 rounded-full border-8 border-green-500 flex items-center justify-center"
  >
    <p class="font-bold text-2xl text-green-600">{{ percentage }}%</p>
    <div
      class="absolute top-0 left-0 w-32 h-32 border-8 border-gray-200 rounded-full"
    ></div>
  </div>
</template>

<script>
export default {
  props: {
    percentage: {
      type: Number,
      required: true,
    },
  },
};
</script>
