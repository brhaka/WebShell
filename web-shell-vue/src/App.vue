<template>
	<div id="app">
		<Terminal />
	</div>
</template>

<script>
import Terminal from './components/Terminal.vue'

export default {
	name: 'App',
	components: {
		Terminal
	}
}
</script>

<style>
	#app {
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
	}

	body {
		margin: 0;
	}
</style>
