<script lang="ts">
	export let techStack;
</script>

<article>
	<h2>Things I'm interested in</h2>
	<p><i>Feel free to connect me if you're interested in them as well</i></p>
	{#each techStack as tech}
		<span class="badge">{tech}</span>
	{/each}
</article>
