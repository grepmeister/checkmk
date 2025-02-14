// Copyright (C) 2023 tribe29 GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the
// terms and conditions defined in the file COPYING, which is part of this
// source code package.

#ifndef NebComment_h
#define NebComment_h

#include "Comment.h"
#include "NebHost.h"
#include "NebService.h"
#include "livestatus/Interface.h"

class NebComment : public IComment {
public:
    explicit NebComment(const Comment &comment)
        : comment_{comment}
        , host_{NebHost{*comment._host}}
        , service_{ToIService(comment_._service)} {}
    [[nodiscard]] int32_t id() const override { return comment_._id; }
    [[nodiscard]] std::string author() const override {
        return comment_._author;
    }
    [[nodiscard]] std::string comment() const override {
        return comment_._comment;
    }
    [[nodiscard]] CommentType entry_type() const override {
        return static_cast<CommentType>(comment_._entry_type);
    }
    [[nodiscard]] std::chrono::system_clock::time_point entry_time()
        const override {
        return comment_._entry_time;
    }

    [[nodiscard]] bool isService() const override {
        return comment_._is_service;
    }
    [[nodiscard]] bool persistent() const override {
        return comment_._persistent;
    }
    [[nodiscard]] CommentSource source() const override {
        return static_cast<CommentSource>(comment_._source);
    }
    [[nodiscard]] bool expires() const override { return comment_._expires; }
    [[nodiscard]] std::chrono::system_clock::time_point expire_time()
        const override {
        return comment_._expire_time;
    }

    [[nodiscard]] const IHost &host() const override { return host_; }
    [[nodiscard]] const IService *service() const override {
        return service_ ? service_.get() : nullptr;
    }

private:
    const Comment &comment_;
    const NebHost host_;
    const std::unique_ptr<const IService> service_;
};

#endif  // NebComment_h
