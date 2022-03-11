<template>
	<div ref="container">
		<div v-for="(input, index) in inputs" :key="index">
			<table ref="main" class="inputTable">
				<tr>
					<td ref="prompts" class="prompt">
						<span class="prompt">{{ prompt }}</span>
					</td>
					<td>
						<textarea class="inputTextarea" ref="inputs" autofocus="true" onblur="this.focus()" @keyup="handleKeyUp($event);" @input="verifyContent($event);adjustInputSize($event.target);" v-model="input.content" autocomplete="nope" spellcheck="false" data-gramm="false" data-gramm_editor="false" data-enable-grammarly="false" />
					</td>
				</tr>
			</table>
		</div>
	</div>
</template>

<script>
import Embedded from "./Embedded.vue"
import Vue from "vue"

export default {
	name: "InputCompName",
	props: ["vmId"],
	data: function () {
		return {
			history: [],
			historyIndex: 0,
			prompt: "~$ ",
			counter: 0,
			reload: false,
			isEmbeddedOpen: false,
			inputs: [{
				content: "",
				index: 0
			}],
			commands: {
				"exit": this.exitCommand,
				"clear": this.clearCommand,
				"search": this.searchCommand,
				"reload": this.exitCommand,
				"reboot": this.exitCommand,
				"restart": this.exitCommand,
				"google": this.googleCommand,
			},
			errors: {
				0x001: "Missing ID",
				0x002: "Expired or invalid VM\nreload, reboot or restart to continue",
				0x003: "VM connection error",
				0x004: "Missing Command",
				0x005: "command not found",
				0x006: "this command requires at least 1 argument",
			},
		}
	},
	created() {
		this.history = document.cookie.replace("History=", "").split(",")
		this.historyIndex = this.history.length

		window.addEventListener("touchstart", () => {
			this.$refs.inputs[this.counter].focus()
		})
		window.addEventListener("click", () => {
			this.$refs.inputs[this.counter].focus()
		})
	},
	methods: {
		log (msg) {
			console.log(msg)
		},
		handleKeyUp (event) {
			if (event.keyCode === 13) { // Enter
				if (event.target.value != "") {
					this.saveToHistory(event)
				}
				this.runCommand(event)
			} else if (!event.shiftKey && event.ctrlKey && event.keyCode === 67) { // CTRL + C (without Shift)
				this.newInput("", false)
			} else if (event.ctrlKey& event.keyCode === 68) { // CRTL + D
				location.reload()
			} else if (event.keyCode === 38) { // Up arrow
				event.target.value = this.fetchHistory(1)
				event.preventDefault()
			} else if (event.keyCode === 40) { // Down arrow
				event.target.value = this.fetchHistory(-1)
				event.preventDefault()
			} else if (event.keyCode === 27) { // Escape
				if (this.isEmbeddedOpen) {
					this.newInput()
					this.isEmbeddedOpen = false
				}
			}
		},
		verifyContent (event) {
			this.$nextTick(function () {
				var value = event.target.value

				value = value.replaceAll("\n", "")

				event.target.value = value
			});
		},
		async runCommand (event) {
			var input = event.target.value
			var command = ""
			var args = []

			input = input.replaceAll("\n", "")

			if (input != "" && input != "Loading...") {
				this.newInput("Loading...", true, false)
				this.$nextTick(() => {
					this.disableCurrentInput()
				})

				if (input.includes(" ")) {
					command = input.substring(0, input.indexOf(" "))
					args = this.getArgs(input)
				} else {
					command = input
				}

				if (command) {
					if (this.commands[command]) {
						this.commands[command](args, command)
					} else {
						this.executeCommand(input, command)
					}
				} else {
					this.newInput()
				}
			} else {
				this.newInput()
			}
		},
		newInput (newContent="", setSize=true, showPrompt=true) {
			this.disableCurrentInput()

			this.inputs.push({
				content: newContent,
				index: ++this.counter
			});

			var staticCounter = this.counter
			this.$nextTick(function () {
				if (setSize) {
					this.adjustInputSize(this.$refs.inputs[staticCounter])
				}
				if (!showPrompt) {
					this.$refs.prompts[staticCounter].style.display = "none"
				}
				this.$refs.inputs[this.counter].focus()
			});
		},
		adjustInputSize (element) {
			element.style.height = "0px"
			element.style.height = (element.scrollHeight)  + "px"
		},
		saveToHistory (event) {
			var value = event.target.value
			var toSave = value

			this.history.push(toSave)
			this.historyIndex = this.history.length

			let d = new Date()
			d.setTime(d.getTime() + 42 * 24 * 60 * 60 * 1000) // Expires in 42 days
			let expires = "expires=" + d.toUTCString()
			document.cookie = "History=" + this.history + ";" + expires + ";path=/"
		},
		fetchHistory (direction) { // Direction (1 Up, -1 Down)
			if (this.history.length <= 1) {
				return ""
			}

			this.historyIndex -= direction

			if (this.historyIndex === this.history.length) {
				return ""
			} else if (this.historyIndex > this.history.length) {
				this.historyIndex += direction
				return ""
			} else if (this.historyIndex < 1) {
				this.historyIndex = 1
			}

			return this.history[this.historyIndex]
		},
		printError (message) {
			this.newInput(message, true, false)
			var staticCounter = this.counter
			this.$nextTick(function() {
				this.$refs.inputs[staticCounter].style.color = "red"
			})
		},
		disableCurrentInput () {
			var staticCounter = this.counter

			if (!this.$refs.inputs[staticCounter]) {
				return
			}

			this.$refs.inputs[staticCounter].setAttribute("onblur", "")
			this.$refs.inputs[staticCounter].setAttribute("autofocus", "false")
			this.$refs.inputs[staticCounter].setAttribute("readonly", "true")
			this.$refs.inputs[staticCounter].setAttribute("keyup", "")
			this.$refs.inputs[staticCounter].setAttribute("input", "")
		},
		getArgs (input) { // Properly splits 'input' into 'args' using spaces, unless inside quotes (double or single)
			var args = input.match(/(?:[^\s"']+|['"][^'"]*["'])+/g)

			for (let i = 0; i < args.length; i++) {
				args[i] = args[i].replaceAll("\"", "")
				args[i] = args[i].replaceAll("'", "")
			}

			return args
		},
		// Commands
		exitCommand () {
			location.reload()
		},
		clearCommand () {
			document.cookie = "History=;"
			this.exitCommand()
		},
		searchCommand (args) {
			this.embedd(args, "https://en.wikipedia.org/wiki/", "search")
		},
		googleCommand (args) {
			this.embedd(args, "https://www.google.com/search?igu=1&q=", "google")
		},
		embedd (args, url, command) {
			if (args.length >= 2) { // First argument is the command
				var ComponentClass = Vue.extend(Embedded)
				var embedded = new ComponentClass({
					propsData: { url: (url + args[1]) }
				})

				this.isEmbeddedOpen = true

				embedded.$mount()
				this.$refs.container.appendChild(embedded.$el)
			} else {
				this.printError(this.errors[0x006] + ": " + command)
				this.$nextTick(() => {
					this.newInput()
				})
			}
		},
		executeCommand(input, command) {
			fetch(`${process.env.VUE_APP_VIRTUALIZER_HOST}/executeCommand?id=${this.vmId}&command=${input}`, {
				method: "GET",
			})
			.then(response => response.json()) // Parses the return to JSON
			.then(data => {
				if (data.return.toString().startsWith("OCI runtime exec failed")) {
					this.printError(this.errors[0x005] + ": " + command)
				} else if (!data.return.toString().startsWith("ERROR:")) {
					this.newInput(data.return, true, false)
				} else {
					var errorCode = data.return.toString().replace("ERROR:", "")
					this.printError(this.errors[parseInt(errorCode)])
				}
			}) // Outputs the return
			.catch(error => {
				if (error.toString().startsWith("SyntaxError")) {
					this.printError(this.errors[0x005] + ": " + command)
				} else {
					this.printError(this.errors[0x003])
				}
			}) // Handles errors
			.then(() => {
				this.$refs.main[this.counter - 1].remove()
				this.$nextTick(() => {
					this.newInput()
				})
			}) // Puts a new input
		}
	}
}
</script>

<style scoped>
.inputTextarea {
	border: none;
	outline: none;
	width: 100%;
	max-width: 100%;
	height: 100%; /* Adjust textarea size to fill all the screen height when typing */
	max-height: 100%;
	overflow-wrap: break-word;
	overflow: auto;
	resize: none;
	padding: 0 0 2px 0;
}

.prompt {
	vertical-align: top;
	width: 18px;
}

.inputTable {
	width: 100%;
}

.prompt {
	color: cyan;
}
</style>
