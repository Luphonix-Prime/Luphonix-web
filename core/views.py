from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from .models import TeamMember, Technology, Project
from .forms import ContactForm
from .github_api import get_repositories

class IndexView(TemplateView):
    """Main landing page view"""
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add key team members and technologies to context
        context['team_members'] = TeamMember.objects.all()[:4]  # Limit to 4 team members
        context['technologies'] = Technology.objects.all().order_by('category', 'order')[:8]
        context['featured_projects'] = Project.objects.all()[:3]  # Featured projects
        return context

class TeamView(ListView):
    """Team members list view"""
    model = TeamMember
    template_name = 'core/team.html'
    context_object_name = 'team_members'

class TechnologiesView(ListView):
    """Technologies/Skills list view"""
    model = Technology
    template_name = 'core/technologies.html'
    context_object_name = 'technologies'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group technologies by category
        technologies_by_category = {}
        for category, _ in Technology.CATEGORY_CHOICES:
            technologies_by_category[category] = Technology.objects.filter(category=category)
        
        context['technologies_by_category'] = technologies_by_category
        return context

class ProjectsView(TemplateView):
    """Projects view with GitHub integration"""
    template_name = 'core/projects.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get projects from database
        context['projects'] = Project.objects.all()
        
        # Get repositories from GitHub
        github_repos = get_repositories(limit=6)
        context['github_repos'] = github_repos
        
        return context

class ContactView(FormView):
    """Contact form view"""
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        # Save message to database
        message = form.save()
        
        # Send email notification
        subject = f"New contact message: {message.subject}"
        email_message = (
            f"From: {message.name} <{message.email}>\n\n"
            f"Subject: {message.subject}\n\n"
            f"Message:\n{message.message}"
        )
        
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Send to default email
                fail_silently=False,
            )
            messages.success(self.request, "Your message has been sent successfully. We'll get back to you soon!")
        except Exception as e:
            messages.error(self.request, "There was an error sending your message. Please try again later.")
        
        return super().form_valid(form)
