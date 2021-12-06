# EdGAIL

This is a working repository on a reinforcement learning approach to generating synthetic learning behavior data.

## EdNet

[EdNet](https://github.com/riiid/ednet) is the dataset of all student-system interactions collected over 2 years by Santa, a multi-platform AI tutoring service with more than 780K users in Korea available through Android, iOS and web.

The goal is to use EdNet to extract an expert policy that will be used to train an [imitation learning agent](https://dl.acm.org/doi/10.1145/3054912). This agent will then model student behavior and learning habits that can be used to expand on the EdNet dataset more efficiently than by using conventional methods.

## State-Action Space

EdNet consists of four datasets with increasing resolution in terms of the actions of students being tracked.

#### EdNet-KT1

- `timestamp` is the moment the question was given, represented as **Unix timestamp in milliseconds**.
- `solving_id` represents each learning session of students corresponds to each bunle. It is a form of single **integer**, starting from `1`.
- `question_id` is the ID of the question that given to student, which is a form of `q{integer}`.
- `user_answer` is the answer that the student submitted, recorded as a character between `a` and `d` inclusively.
- `elapsed_time` is the time that the students spends on each question in **milliseconds**.

#### EdNet-KT2

- `action_type` is one of the following: `enter`, `respond`, and `submit`.
    - `enter` is recorded when student first receives and views a question bundle through UI.
    - `respond` is recorded when the student selects an answer choice to one of the questions in the bundle. A student can respond to the same question multiple times. In this case, only the last response before submitting his final answer is considered as his response.
    - `submit` is recorded when the student submits his final answers to the the given bundle.
- `item_id` is The ID of item involved with the action. For EdNet-KT2, only the IDs of questions and bundles are recorded. A bundle is assigned for actions of type `enter` and `submit`.
- `source` shows *where* the student solve a question or watch a lecture in *Santa* UI. There are several sources in *Santa* that students can solve questions or watch lectures. For KT2, only the sources that provides question-solving environments are recorded.
    - In `sprint`, students choose a part that they want to study. After that, they can only solve questions belongs to the part that they choose, until they change to different part or select different source.
    - For each day, *Santa* recommends questions and lectures based on each student's current knowledge status, i.e. correctness probabilities predicted by the Collaborative Filtering model. Such source is called *Today's Recommendation*. Questions that belong to particular parts can be recommended, `todays_recommendation::sprint`, `todays_recommendation::review_quiz`
    - Once the number of incorrect answers to questions with particular tags exceeds certain threshold, *Santa* suggests lectures and questions with corresponding tags. Such suggestion is recorded as `adaptive_offer`. It also offers lectures and questions if the average correctness rate of questions with particular tags decreased by more than a certain threshold.
    - *All Parts* is a source that students solve questions that *Santa* recommends following a certain algorithm, from all possible candidates. This is recorded as `tutor`.
    - The student can re-do the questions that he already solved before using *review* system, which is recorded as `in_review`.
- `user_answer` is recorded when `action_type` is `respond`, which stands for the student's submitted answer. It is one of the alphabets `a`, `b`, `c`, and `d`.
- `platform` shows where the student used *Santa*, which is either **mobile** or **web**.

#### EdNet-KT3

- Reading Explanations
    - After each student solves given questions, corresponding explanations are given to him. The sources of explanations for questions from `sprint` and `review` are recorded as `after_sprint` and `after_review`, respectively. One can also re-read explanations of questions that he solved from `my_note`.
    - Whenever a student enters the explanation view in *Santa* UI or exits the view, a corresponding action of type `enter` and `quit` with explanation ID as `item_id` is recorded. Note that the explanation ID is exactly same as the bundle ID.
- Watching Lectures
    - There are two possible sources that the student can watch a lecture: `archive`, `adaptive_offer`, and `todays_recommendatin::lecture`. He can access all the possible lectures from `archive`. Also, *Santa* can suggest lectures by *Today's recommendation* or *adaptive offer* along with questions.
    - Whenever a student plays a lecture video or stops watching the video, a corresponding action of type `enter` and `quit` with lecture ID as `item_id` is recorded.

#### EdNet-KT4

- `erase_choice`, `undo_erase_choice`
    - For user's convenience, a student can hide an answer choice by erasing it. He can also undo his action to consider the choice again. The act of erasing a choice and undoing it are given as actions of type `erase_choice` and `undo_erase_choice` respectively. The answer choice erased/un-erased is supplied in the `user_answer` column.
- `play_audio`, `pause_audio`, `play_video`, `pause_video`
    - A student can play or pause a given multimedia asset. For videos, he can also navigate to different moments of the video by moving his cursor to different places. Such actions are denoted as one of the action types `play_audio`, `pause_audio`, `play_video` or `pause_video`. A column `cursor_time` is added to EdNet-KT4, to represent the moment where he has played or paused the media.
- `pay`, `refund`
    - By default, a free user is offered 10 questions of Part 2 and 5 each daily. By purchasing a payment item, the student have full access to questions of all parts. A table of payment items is provided separately (see below). Items of type `pass` allows solving all questions for the time `duration` in milliseconds. Items of type `paygo` allows student to solve the specific number of bundles denoted by column `number_of_bundles`.
- `enroll_coupon`
    - A student may enter his promotion coupon code to receive corresponding benefits. The ID of his coupon and the time he entered the coupon is recorded as an action of type `enroll_coupon`. A table of coupons is provided separately (see below).

## Actions

From the sections above, the following list of actions is extracted:
- `enter` (view a question bundle **or** the explanation)
- `respond` (select answer)
- `submit` (submit answer)
- `quit` (quit explanation view)
- `erase_choice`
- `undo_erase_choice`
- `play_audio`
- `pause_audio`
- `play_video`
- `pause_video`
- `pay`
- `refund`
- `enroll_coupon`