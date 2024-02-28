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

<div class="row">
	<div class="col-3">
		<img height="300" alt="Me" src={me} />
	</div>
	<div class="col">
		<h1>Alexander Sidorov</h1>
		<p>Forthcoming personal page, development in progress.</p>
		<p><a href="https://sidorov.dev">About</a></p>
		I am software engineer with 12+ years of experience. Customer experience, user experience, quality
		and reliability are the areas I'm focusing. Clean Architecture apologist. Full-stack wannabe. Mentor
		for good people. Apple fanboy. Father of two kids. Sailor, boxer, driver - however currently in the
		end of a long-term "vacation". In the meantime, backgammon player.
	</div>
	<div class="col-2">
		<p><a href="https://github.com/tgrx">GitHub</a></p>
		<p><a href="https://www.linkedin.com/in/alexnsidorov/">LinkedIn</a></p>
		<p><a href="https://t.me/jesuisalexandre">Telegram</a></p>
	</div>
</div>

<div class="row">
	<div class="col">
		<pre>{$codeSnippet}</pre>
	</div>
	<div class="col-5">
		<p>Feel free to connect if you're interesting in these:</p>
		<p>
			{#each data.technologies as tech}
				<span class="badge text-bg-success my-1 mx-1">{tech}</span>
			{/each}
		</p>
	</div>
</div>
