define([
    'backbone',
    'jquery',], function (Backbone, $) {
    return Backbone.View.extend({
        minChangesetComment: 10, // minimum character of changeset comment
        minChangesetSource: 5, // minimum character of changeset source
        initialize: function () {
            this.$modal = $('#changeset-comment');
            this.$modalSubmit = $('#changeset-comment-submit');
            this.$modalCancel = $('#changeset-comment-cancel');
            this.$modalCommentInput = $('#changeset-comment-input');
            this.$modalSourceInput = $('#changeset-comment-source-input');
            this.$modalCommentInputError = $('#changeset-comment-input-error');
            this.$modalSourceInputError = $('#changeset-comment-source-input-error');
        },
        /**
         * resetting modal state
         */
        reset: function () {
            this.$modalCommentInput.val('');
            this.$modalSourceInput.val('');
            this.$modalCommentInputError.hide();
            this.$modalSourceInputError.hide();
        },
        /***
         * Show function
         * If ok, it will call submit funtion with data
         * If cancel, it will call cancel Function
         * @param submitFunction
         * @param cancelFunction
         */
        show: function (submitFunction, cancelFunction) {
            let self = this;
            this.$modal.modal('show');
            this.$modal.on('shown.bs.modal', function () {
                self.reset();

                // submit event
                self.$modalSubmit.off('click');
                self.$modalSubmit.click(function () {
                    self.$modalCommentInputError.hide();
                    self.$modalSourceInputError.hide();
                    let data = {
                        'comment': self.$modalCommentInput.val(),
                        'source': self.$modalSourceInput.val()
                    };
                    let valid = true;
                    if (data['comment'].length <= self.minChangesetComment) {
                        self.$modalCommentInputError.show();
                        valid = false
                    }
                    if (data['source'].length <= self.minChangesetSource) {
                        self.$modalSourceInputError.show();
                        valid = false
                    }
                    if (valid) {
                        self.reset();
                        self.$modal.modal('hide');
                        if (submitFunction) {
                            submitFunction(data);
                        }
                    }
                })

                // cancel event
                self.$modalCancel.off('click');
                self.$modalCancel.click(function () {
                    self.reset();
                    self.$modal.modal('hide');
                    if (cancelFunction) {
                        cancelFunction()
                    }
                })
            })
        }
    })
});

