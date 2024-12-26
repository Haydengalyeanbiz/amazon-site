<template>
	<div class="homepage-container">
		<div class="posts-container">
			<div
				class="post-card"
				v-for="post in posts"
				:key="post.id"
			>
				<div class="post-img-title">
					<img
						:src="post.image_url"
						alt="Product Image"
						class="post-image"
					/>
					<h3 class="post-title">{{ post.title }}</h3>
				</div>
				<div class="post-info-holder">
					<p class="post-description">{{ post.description }}</p>
					<div class="post-actions">
						<button
							class="visit-link-btn"
							@click="goToLink(post.link_url)"
						>
							Visit Product
						</button>
						<div
							v-if="isAuthenticated && post.user_id === user.id"
							class="user-controls"
						>
							<button
								class="edit-btn"
								@click="goToEditPage(post.id)"
							>
								Edit
							</button>
							<button
								class="delete-btn"
								@click="openDeleteModal(post.id)"
							>
								Delete
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Pagination Controls -->
		<div class="pagination-controls">
			<button
				:disabled="!hasPrevPage"
				@click="loadPage(currentPage - 1)"
				class="pagination-btn"
			>
				Previous
			</button>
			<span>Page {{ currentPage }} of {{ totalPages }}</span>
			<button
				:disabled="!hasNextPage"
				@click="loadPage(currentPage + 1)"
				class="pagination-btn"
			>
				Next
			</button>
		</div>

		<!-- Delete Modal -->
		<div
			v-if="showDeleteModal"
			class="modal-overlay"
		>
			<div class="modal-content">
				<h3>Are you sure you want to delete this post?</h3>
				<button
					@click="confirmDelete"
					class="confirm-delete-btn"
				>
					Yes, Delete
				</button>
				<button
					@click="showDeleteModal = false"
					class="cancel-delete-btn"
				>
					Cancel
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
	name: 'HomePage',
	data() {
		return {
			showDeleteModal: false,
			selectedPostId: null,
		};
	},
	computed: {
		...mapState([
			'posts',
			'currentPage',
			'totalPages',
			'hasPrevPage',
			'hasNextPage',
			'user',
			'isAuthenticated',
		]),
	},
	methods: {
		...mapActions(['fetchPosts', 'deletePost']),
		goToLink(link) {
			console.log('Navigating to:', link);
			window.open(link);
		},
		goToEditPage(postId) {
			this.$router.push({ name: 'EditProductPage', params: { id: postId } });
		},
		openDeleteModal(postId) {
			this.selectedPostId = postId;
			this.showDeleteModal = true;
		},
		async confirmDelete() {
			try {
				await this.deletePost(this.selectedPostId);
				this.showDeleteModal = false;
				console.log(`Deleted post with ID: ${this.selectedPostId}`);
			} catch (error) {
				console.error('Failed to delete post:', error);
			}
		},
		async loadPage(page) {
			try {
				// Call the fetchPosts action to fetch data and update the state
				await this.fetchPosts({
					page,
					perPage: 12,
				});
			} catch (error) {
				console.error('Error loading page:', error);
			}
		},
	},
	created() {
		this.fetchPosts({ page: this.currentPage || 1, perPage: 12 });
	},
};
</script>

<style scoped>
.homepage-container {
	display: flex;
	flex-direction: column;
	justify-content: center;
	background-color: var(--primary-light);
	padding: 10dvh 0 8dvh;
	height: auto;
}

.posts-container {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	justify-content: center;
	margin: 0 auto;
	gap: 2rem;
	height: auto;
}

.post-card {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	border-radius: 8px;
	max-width: 360px;
	text-align: center;
	background-color: var(--primary-dark);
	border: 4px solid var(--secondary-dark);
}

.post-img-title {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0.5rem;
	position: relative;
}

.post-image {
	width: 100%;
	height: auto;
	max-height: 360px;
	object-fit: cover;
	border-radius: 6px;
}

.post-info-holder {
	display: flex;
	flex-direction: column;
	padding: 0.5rem 1rem;
	justify-content: space-between;
	align-items: center;
	height: 100%;
}

.post-title {
	max-width: 360px;
	font-size: var(--fs-medium);
	font-weight: var(--fw-bold);
	background-color: var(--primary-light);
	border-radius: 12px;

	padding: 0.3rem 0.5rem;
	position: absolute;
	bottom: 4px;
}

.post-price,
.post-description {
	color: var(--primary-light);
}

.post-actions {
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 0.5rem;
}

.visit-link-btn {
	width: fit-content;
	padding: 0.5rem;
	border-radius: 10px;
	border: none;
	background-color: var(--primary-dark);
	color: var(--secondary-light);
	transition: var(--transition);
}

.visit-link-btn:hover {
	background-color: var(--secondary-light);
	color: var(--primary-light);
}

.user-controls {
	display: flex;
	gap: 0.5rem;
}

.edit-btn,
.delete-btn {
	padding: 0.3rem 0.5rem;
	border-radius: 12px;
	border: none;
	background-color: var(--primary-light);
}

.edit-btn:hover {
	background-color: var(--secondary-dark);
}

.delete-btn:hover {
	background-color: var(--danger-clr);
}

/* ? MODAL Styling */
.modal-overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0.5);
	display: flex;
	justify-content: center;
	align-items: center;
}

.modal-content {
	background: var(--primary-dark);
	color: var(--primary-light);
	padding: 2rem;
	border-radius: 10px;
	text-align: center;
}

.confirm-delete-btn {
	background-color: var(--danger-clr);
	color: white;
	border: none;
	border-radius: 12px;
	padding: 0.5rem 1rem;
	cursor: pointer;
	margin-right: 1rem;
}

.cancel-delete-btn {
	background-color: var(--primary-dark);
	color: white;
	border: none;
	padding: 0.5rem 1rem;
	cursor: pointer;
}

.pagination-controls {
	display: flex;
	justify-content: center;
	align-items: center;
	margin-top: 20px;
}

.pagination-btn {
	border: none;
	background-color: var(--primary-light);
	color: var(--primary-dark);
	margin: 0 10px;
	padding: 5px 10px;
	transition: var(--transition);
}

.pagination-btn:hover {
	color: var(--secondary-dark);
}

/* !TABLETS */
@media (max-width: 1200px) {
	.posts-container {
		grid-template-columns: repeat(2, 1fr); /* 2 items per row */
		padding: 15px;
	}

	.post-card {
		font-size: 16px;
	}
}

/* !PHONES */
@media (max-width: 780px) {
	.posts-container {
		grid-template-columns: repeat(1, 1fr); /* 2 items per row */
		padding: 15px;
	}

	.post-card {
		font-size: 16px;
	}
}
</style>
