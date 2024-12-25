<template>
	<div id="app">
		<div class="navbar">
			<router-link
				class="navbar-logo"
				to="/"
				>IndyMamaDeals</router-link
			>

			<!-- Hamburger Icon -->
			<div
				class="hamburger"
				v-if="isMobile"
				@click="toggleMenu"
			>
				<span></span>
				<span></span>
				<span></span>
			</div>

			<!-- Links -->
			<div
				class="navbar-items"
				:class="{ open: menuOpen }"
				v-if="!isMobile || menuOpen"
			>
				<!-- Links for logged-in users -->
				<router-link
					v-if="isAuthenticated"
					to="/find-store-product"
				>
					Add Store Product
				</router-link>
				<router-link
					v-if="isAuthenticated"
					to="/find-product"
				>
					Add Amazon Product
				</router-link>
				<!-- Logout Button for logged-in users -->
				<button
					class="logout-btn"
					v-if="isAuthenticated"
					@click="logout"
				>
					Logout
				</button>
				<!-- Social Links visible to everyone -->
				<div
					class="social-links"
					v-if="!isAuthenticated"
				>
					<a href="https://www.facebook.com/indycouponmama">Facebook</a>
					<a href="https://instagram.com/indy_mama_deals">Instagram</a>
				</div>
			</div>
		</div>
		<router-view />
		<FooterComponent />
	</div>
</template>

<script>
import FooterComponent from './components/FooterComponent.vue';
import { mapState, mapActions } from 'vuex';

export default {
	name: 'App',
	components: {
		FooterComponent,
	},
	data() {
		return {
			menuOpen: false, // Tracks whether the hamburger menu is open
			isMobile: false, // Tracks whether the screen size is mobile
		};
	},
	computed: {
		...mapState(['isAuthenticated']),
	},
	methods: {
		...mapActions(['logout']),
		toggleMenu() {
			this.menuOpen = !this.menuOpen; // Toggles menu visibility
			console.log('Menu toggled:', this.menuOpen); // Debug menu state
		},
		handleResize() {
			this.isMobile = window.innerWidth < 780; // Adjusts `isMobile` based on screen size
			if (!this.isMobile) {
				this.menuOpen = false; // Close the menu if resizing to desktop
			}
		},
	},
	mounted() {
		this.handleResize(); // Check screen size on load
		window.addEventListener('resize', this.handleResize); // Listen for screen size changes
	},
	beforeUnmount() {
		window.removeEventListener('resize', this.handleResize); // Cleanup event listener
	},
};
</script>

<style scoped>
.navbar {
	position: fixed;
	z-index: 1000;
	height: 8dvh;
	width: 100%;
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0 2rem;
	background-color: var(--primary-dark);
	border-bottom: solid 6px var(--secondary-dark);
	box-sizing: border-box;
}

.navbar-logo {
	font-family: var(--header-ff);
}

.social-links {
	display: flex;
	gap: 1rem;
}

.navbar-items {
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 1.5rem;
}

.navbar-items.open {
	display: flex; /* Show items when menuOpen is true */
}

.hamburger {
	display: none;
	flex-direction: column;
	gap: 0.3rem;
	cursor: pointer;
}

.hamburger span {
	width: 25px;
	height: 3px;
	background-color: white;
}

nav a {
	font-family: var(--header-ff);
}

nav a.router-link-exact-active {
	font-weight: bold;
}

nav a {
	transition: var(--transition);
}

nav a:hover {
	color: var(--secondary-light);
}

.logout-btn {
	font-family: var(--header-ff);
	border: none;
	color: var(--primary-light);
	background-color: var(--primary-dark);
	transition: var(--transition);
}

.logout-btn:hover {
	color: var(--secondary-dark);
}

@media (max-width: 780px) {
	.social-links {
		padding: 0.3rem 0;
		flex-direction: column;
		gap: 1rem;
	}

	.navbar-items {
		gap: 0.5rem;
	}

	.navbar-items {
		display: none; /* Hide by default on mobile */
		flex-direction: column;
		gap: 1rem;
		padding: 1rem 0;
		background-color: var(--primary-dark);
		position: absolute;
		top: 8dvh;
		width: 100%;
		left: 0;
		z-index: 1000;
	}

	.navbar-items.open {
		display: flex; /* Show when menuOpen is true */
	}
	.hamburger {
		display: flex; /* Show hamburger menu icon */
	}
}
</style>
