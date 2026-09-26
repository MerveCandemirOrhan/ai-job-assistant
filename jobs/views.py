from django.shortcuts import render, get_object_or_404
from .models import Job, CV
from django.db.models import Q
from django.core.paginator import Paginator
from job_analyzer import (
    analyze_job,
    analyze_cv,
    extract_cv_text,
    match_cv_to_job,
)
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, CVUploadForm
from django.contrib.auth.decorators import login_required

def job_list(request):
    search = request.GET.get("search")
    location = request.GET.get("location")
    job_type = request.GET.get("job_type")

    jobs = Job.objects.all()

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(location__icontains=search) |
            Q(description__icontains=search)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    jobs = jobs.order_by("-created_at")
    paginator = Paginator(jobs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "jobs/job_list.html",
        {"jobs": page_obj}
)
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    cv = CV.objects.filter(user=request.user).first()

    # İş ilanının başlık ve açıklamasını AI analizine gönder
    text = f"{job.title} {job.description}"

    if job.ai_analysis:
        # Daha önce analiz edilmişse veritabanındaki sonucu kullan
        analysis = job.ai_analysis
    else:
        # İlk kez analiz ediliyorsa AI'ya gönder
        analysis = analyze_job(text)

        # AI sonucunu veritabanına kaydet
        job.ai_analysis = analysis
        job.save()

    if cv:
        cv_analysis = cv.ai_analysis

        match_result = match_cv_to_job(
            cv_analysis,
            analysis,
        )
    else:
        match_result = None

    return render(
        request,
        "jobs/job_detail.html",
        {
            "job": job,
            "analysis": analysis,
            "match_result": match_result,
        }
    )

def cv_detail(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id, user=request.user)

    if cv.ai_analysis:
        analysis = cv.ai_analysis
    else:
        text = extract_cv_text(cv.file.path)
        analysis = analyze_cv(text)

        cv.ai_analysis = analysis
        cv.save()

    return render(
        request,
        "jobs/cv_detail.html",
        {
            "cv": cv,
            "analysis": analysis,
        }
    )

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )

@login_required
def upload_cv(request):
    if request.method == "POST":
        form = CVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()

            return redirect("job_list")
    else:
        form = CVUploadForm()

    return render(
        request,
        "jobs/upload_cv.html",
        {"form": form},
    )