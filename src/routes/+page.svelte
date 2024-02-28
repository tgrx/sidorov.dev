<script lang="ts">
	import me from '$lib/static/me.webp';
	import { readable } from 'svelte/store';

	export let data;

	const codeSnippet = readable(data.codeSnippet, (set) => {
		const iid = setInterval(() => {
			const idx = Math.floor(Math.random() * data.codeSnippets.length);
			set(data.codeSnippets[idx]);
		}, 8000);

		return () => {
			clearInterval(iid);
		};
	});
</script>

<div class="container x">
	<div class="x" style:grid-row="1/2" style:grid-column="1/2">
		<img height="300" alt="Me" src={me} />
	</div>
	<div class="x" style:grid-row="1/2" style:grid-column="2/3">
		<h1>Alexander Sidorov</h1>
		<p>Forthcoming personal page, development in progress.</p>
		<p><a href="https://sidorov.dev">About</a></p>
		I am software engineer with 12+ years of experience. Customer experience, user experience, quality
		and reliability are the areas I'm focusing. Clean Architecture apologist. Full-stack wannabe. Mentor
		for good people. Apple fanboy. Father of two kids. Sailor, boxer, driver - however currently in the
		end of a long-term "vacation". In the meantime, backgammon player.
	</div>
	<div class="x" style:grid-row="1/2" style:grid-column="3/4">
		<p><a href="https://github.com/tgrx">GitHub</a></p>
		<p><a href="https://www.linkedin.com/in/alexnsidorov/">LinkedIn</a></p>
		<p><a href="https://t.me/jesuisalexandre">Telegram</a></p>
	</div>


	<div class="x" style:grid-row="2/3" style:grid-column="1/2">
		<pre>{$codeSnippet}</pre>
	</div>
	<div class="x" style:grid-row="2/3" style:grid-column="2/3">
		<p>Feel free to connect if you're interesting in these:</p>
		<p>
			{#each data.technologies as tech}
				<span class="badge text-bg-success my-1 mx-1">{tech}</span>
			{/each}
		</p>
	</div>

</div>


<style>
	.container {
		--auto-grid-min-size: 20rem;
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(var(--auto-grid-min-size), 1fr));
		grid-gap: 1rem;
	}

	.x {
		border-color:fuchsia;
		border-width: 1px;
		border-style: solid;
	}
</style>