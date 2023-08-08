from django.views import generic
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.forms.models import inlineformset_factory
# from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Record, RecordFile
from .forms import RecordForm   # , RecordUpdateForm
from .decorators import user_is_record_owner
    
@login_required
def record_list_view(request):
    records = Record.objects.filter(owner=request.user)

    context = {
        "records": records
    }

    return render(request, "records/record_list.html",context)
    

@login_required
@user_is_record_owner
def record_detail_view(request, pk):
    record_obj = Record.objects.get(id=pk)

    context = {
        "record": record_obj
    }

    return render(request, "records/record_detail.html",context)


@login_required
def record_search_view(request):

    query_dict = request.GET
    query = query_dict.get("q")

    if query:
        new_search = False
        results = Record.objects.filter(title__icontains=query).filter(owner=request.user)
    else:
        results = None
        new_search = True

    context = {
        "results": results,
        "new_search": new_search
    }
    
    return render(request, "records/record_search.html", context)


@login_required
def record_create_view(request):
    form = RecordForm(request=request)
    
    if request.method == "POST":
        form = RecordForm(request.POST, request=request)

        if form.is_valid():
            new_rec = form.save(commit=False)
            new_rec.owner = request.user
            new_rec.save()

            return redirect(reverse("record-details", kwargs={"pk": new_rec.id}))

    context = {"form": form}

    return render(request, "records/record_create.html",context)


@login_required
@user_is_record_owner
def record_update_view(request, pk):                                         
    rec = get_object_or_404(Record, id=pk)
    form = RecordForm(instance=rec, request=request)                                                               

    if request.method == "POST":
        form = RecordForm(request.POST, instance=rec, request=request)
        if form.is_valid():
            form.save()
            return redirect(reverse("record-details", kwargs={"pk": pk}))
        
    context = {"form":form, "record":rec}

    return render(request, 'records/record_update.html', context)


@login_required
@user_is_record_owner
def record_delete_view(request, pk):
    rec = get_object_or_404(Record, id = pk)
 
    if request.method =="POST":
        rec.delete()
        return redirect(reverse("record-list"))

    context = {'record': rec}
 
    return render(request, "records/record_confirm_delete.html", context=context)
