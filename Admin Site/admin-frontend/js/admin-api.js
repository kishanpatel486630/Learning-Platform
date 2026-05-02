const API_BASE = "http://localhost:5001/api";
// Admin fetches ALL roadmaps (published + drafts) unlike user site which only gets published

const AdminAPI = {
    getToken() {
        return localStorage.getItem("adminToken");
    },
    
    async request(endpoint, options = {}) {
        const token = this.getToken();
        const headers = {
            "Content-Type": "application/json",
            ...options.headers
        };
        
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            localStorage.removeItem("adminToken");
            window.location.href = "index.html"; // redirect to login
        }
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "An error occurred");
        }
        return data;
    },

    // Auth
    login(email, password) {
        return this.request("/auth/login", {
            method: "POST",
            body: JSON.stringify({ email, password })
        });
    },

    // Roadmaps
    getRoadmaps() {
        return this.request("/roadmaps/");
    },
    
    createRoadmap(data) {
        return this.request("/roadmaps/", {
            method: "POST",
            body: JSON.stringify(data)
        });
    },
    
    updateRoadmap(id, data) {
        return this.request(`/roadmaps/${id}`, {
            method: "PUT",
            body: JSON.stringify(data)
        });
    },

    togglePublish(id, is_published) {
        return this.request(`/roadmaps/${id}/publish`, {
            method: "POST",
            body: JSON.stringify({ is_published })
        });
    },
    
    deleteRoadmap(id) {
        return this.request(`/roadmaps/${id}`, {
            method: "DELETE"
        });
    },

    // Users
    getUsers() {
        return this.request("/users/");
    },
    
    banUser(id) {
        return this.request(`/users/${id}/ban`, {
            method: "POST"
        });
    },

    unbanUser(id) {
        return this.request(`/users/${id}/unban`, {
            method: "POST"
        });
    }
};

window.AdminAPI = AdminAPI;
