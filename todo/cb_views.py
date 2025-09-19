from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from todo.models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    """todo list"""
    queryset = Todo.objects.all()
    template_name = 'todo_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        if self.request.user.is_superuser:
            queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return queryset


class TodoDetailView(LoginRequiredMixin, DetailView):
    """todo detail"""
    model = Todo
    template_name = 'todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = {
            'todo': self.object.__dict__
        }
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    """todo 생성"""
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date']
    template_name = 'todo_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    """todo 수정"""
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']
    template_name = 'todo_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    """todo 삭제"""
    model = Todo
    success_url = reverse_lazy('cbv_todo_list')

    """get 요청 시 템플릿을 렌더링하지 않고 바로 삭제"""
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

