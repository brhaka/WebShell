<template>
	<div ref="rootContainer" class="terminal">
		<span ref="connectMsg">Connecting...</span>
		<span ref="errorAlert" style="color: red;display: none;">Unable to establish a connection with a VM</span>
		<span ref="secondsMsg" style="display: none;">Retrying in <span ref="seconds">0</span> seconds...</span>
	</div>
</template>

<script>
	import Input from "./Input.vue"
	import Vue from "vue"

	export default {
		name: "TerminalCompName",
		data: function () {
			return {
				secondsPerAttempt: 4,
				attempts: 0,
			}
		},
		mounted() {
			this.connect()
		},
		methods: {
			connect () {
				this.$refs.connectMsg.style.display = "block"

				fetch(`http://localhost:8000/start`, {
				method: "GET"
				})
				.then(response => response.json()) // Parses the return to JSON
				.then(data => {
					this.$refs.connectMsg.innerHTML = "Connected"
					this.$refs.connectMsg.style.color = "lightgreen"
					this.$refs.errorAlert.remove()
					this.$refs.secondsMsg.remove()

					this.attempts = 0 // Resets the counter

					var ComponentClass = Vue.extend(Input)
					var input = new ComponentClass({
						propsData: { vmId: data.id }
					})

					input.$mount()
					this.$refs.rootContainer.appendChild(input.$el)
				}) // Outputs the return
				.catch(() => {
					this.$refs.connectMsg.style.display = "none"
					this.$refs.errorAlert.style.display = "block"
					this.$refs.secondsMsg.style.display = "block"

					this.attempts = this.attempts + 1
					this.updateSeconds(0)
				}) // Handles errors
			},
			updateSeconds (elapsed) {
				var remaining = (this.secondsPerAttempt * this.attempts) - elapsed

				if (remaining < 0) {
					this.connect()
					return
				}

				this.$refs.seconds.innerHTML = remaining
				console.log(remaining)

				setTimeout(() => {
					this.updateSeconds(++elapsed)
				}, 1000)
			}
		}
	}
</script>

<style scope>
	html, body {
		margin: 0;
		overscroll-behavior: none;
	}

	.terminal {
		height: 100vh;
		max-height: 100vh;
		width: 100vw;
		max-width: 100vw;
	}

	.terminal, .terminal * {
		background-color: #000;
		color: #fff;
		font-family: monospace;
		font-size: 15px;
	}
</style>
