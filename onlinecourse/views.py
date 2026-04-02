from .models import Course, Enrollment, Submission, Choice


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    selected_ids = extract_answers(request)

    submission.choices.set(selected_ids)
    submission.save()

    return redirect('onlinecourse:exam_result', course.id, submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_ids = submission.choices.values_list('id', flat=True)
    questions = course.question_set.all()

    total = 0
    score = 0

    for question in questions:
        total += question.grade
        if question.is_get_score(selected_ids):
            score += question.grade

    context = {
        'course': course,
        'questions': questions,
        'score': score,
        'total': total,
        'selected_ids': list(selected_ids)
    }

    return render(request, 'onlinecourse/exam_result.html', context)


