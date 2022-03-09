<template>
	<div class="embedded">
		<iframe :src="url"></iframe>
		<div>Press ESC to close</div>
	</div>
</template>

<script>
export default {
	name: "EmbeddedCompName",
	props: ["url"],
	mounted() {
		let self = this

		window.addEventListener("keydown", function(event) {
			if (event.code == "Escape") {
				self.$destroy();
				if (self.$el.parentNode) {
					self.$el.parentNode.removeChild(self.$el);
				}
			}
		})
	}
}
</script>

<style scoped>
.embedded {
	width: 100vw;
	height: 100vh;
	position: fixed;
	top: 0;
}

.embedded iframe {
	width: 100%;
	height: 100%;
	border: 0;
}

.embedded div {
	width: 100%;
	bottom: 0;
	position: absolute;
	text-align: center;
	padding-top: 5px;
	padding-bottom: 5px;
}
</style>
