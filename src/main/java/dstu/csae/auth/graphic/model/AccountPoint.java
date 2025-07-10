package dstu.csae.auth.graphic.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "account_point")
@IdClass(AccountPointId.class)
@Getter
@Setter
public class AccountPoint {

    @Id
    @ManyToOne
    @JoinColumn(name = "account_id", nullable = false)
    private Account account;

    @Id
    @Column(nullable = false)
    private Integer x;

    @Id
    @Column(nullable = false)
    private Integer y;

    @Column(name = "position_index", nullable = false)
    private Integer positionIndex;

    @Column(nullable = false, columnDefinition = "text")
    private String hash;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    public void prePersist() {
        createdAt = LocalDateTime.now();
    }

}

