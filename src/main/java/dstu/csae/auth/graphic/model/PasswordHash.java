package dstu.csae.auth.graphic.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "password_hash")
@IdClass(PasswordHashId.class)
@Getter
@Setter
public class PasswordHash {

    @Id
    @ManyToOne
    @JoinColumn(name = "account_id", nullable = false)
    private Account account;

    @Id
    @Column(nullable = false, columnDefinition = "text")
    private String hash;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    public void prePersist() {
        createdAt = LocalDateTime.now();
    }

}
