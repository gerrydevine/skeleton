from django.views import generic
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Record, File
from .forms import RecordCreateForm, RecordUpdateForm
from .decorators import user_is_record_owner

# FileFormset = inlineformset_factory(
#     Record, File, fields=('filename',), extra=2
# )


# class RecordListView(LoginRequiredMixin, generic.ListView):
#     model = Record

#     def get_queryset(self):
#         return Record.objects.filter(owner=self.request.user)
    

# class RecordDetailView(LoginRequiredMixin, generic.DetailView):
#     model = Record

#     def get_queryset(self):
#         return Record.objects.filter(owner=self.request.user)
    

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

    if request.method == "POST":
        form = RecordCreateForm(request.POST, request=request)

        if form.is_valid():
            new_rec = form.save(commit=False)
            new_rec.owner = request.user
            new_rec.save()

            return redirect(reverse("record-details", kwargs={"pk": new_rec.id}))

    form = RecordCreateForm(request=request)
    context = {"form": form}

    return render(request, "records/record_create.html",context)


# @login_required
# @user_is_record_owner
# def record_update_view(request, pk):
#     context = {}

#     if request.method == 'POST':
#         form = RecordForm(request.POST, request=request)
#     else:
#         form = RecordForm(request=request)

#     context = {"form": form}

#     if form.is_valid():
#         updated_rec = form.save(commit=False)
#         updated_rec.owner = request.user
#         updated_rec.save()

#         return redirect(reverse("record-details", kwargs={"pk": updated_rec.id}))

#     return render(request, "records/record_update.html",context=context)


# @login_required
# @user_is_record_owner
# def record_update_view(request, pk):
#     # dictionary for initial data with
#     # field names as keys
#     context ={}
 
#     # fetch the object related to passed id
#     obj = get_object_or_404(Record, id = pk)
 
#     # pass the object as instance in form
#     form = RecordForm(request.POST or None, request=request)
 
#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return redirect(reverse("record-details", kwargs={"pk": pk}))
 
#     # add form dictionary to context
#     context["form"] = form
 
#     return render(request, "update_view.html", context)


@login_required
@user_is_record_owner
def record_update_view(request, pk):                                         
    rec = get_object_or_404(Record, id=pk)
    form = RecordUpdateForm(instance=rec, request=request)                                                               

    if request.method == "POST":
        form = RecordUpdateForm(request.POST, instance=rec, request=request)
        if form.is_valid():
            form.save()
            return redirect(reverse("record-details", kwargs={"pk": pk}))
        
    context = {"form":form}

    return render(request, 'records/record_update.html', context)


# class RecordCreateView(LoginRequiredMixin, CreateView):
#     model = Record
#     form_class = RecordCreateForm

#     # def get_context_data(self, **kwargs):
#     #     data = super().get_context_data(**kwargs)
#     #     if self.request.POST:
#     #         data["files"] = FileFormset(self.request.POST)
#     #     else:
#     #         data["files"] = FileFormset()

#     #     return data

#     # Sending user object to the form for validation purposes
#     def get_form_kwargs(self):
#         kwargs = super(RecordCreateView, self).get_form_kwargs()
#         kwargs.update({'owner': self.request.user})
#         return kwargs
    
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)


# class RecordUpdateView(LoginRequiredMixin, UpdateView):
#     model = Record
#     form_class = RecordUpdateForm

#     def get_queryset(self):
#         return Record.objects.filter(owner=self.request.user)
    
#     # Sending user object to the form for validation purposes
#     def get_form_kwargs(self):
#         kwargs = super(RecordUpdateView, self).get_form_kwargs()
#         kwargs.update({'owner': self.request.user})
#         return kwargs
    
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)


# class RecordDeleteView(LoginRequiredMixin, DeleteView):
#     model = Record
#     success_url = reverse_lazy('record-list')

#     def get_queryset(self):
#         return Record.objects.filter(owner=self.request.user)

@login_required
@user_is_record_owner
def record_delete_view(request, pk):
    rec = get_object_or_404(Record, id = pk)
 
    if request.method =="POST":
        rec.delete()
        return redirect(reverse("record-list"))

    context = {'record': rec}
 
    return render(request, "records/record_confirm_delete.html", context=context)


# class FileDetailView(LoginRequiredMixin, generic.DetailView):
#     model = File

#     def get_queryset(self):
#         return File.objects.filter(record=self.request.record)