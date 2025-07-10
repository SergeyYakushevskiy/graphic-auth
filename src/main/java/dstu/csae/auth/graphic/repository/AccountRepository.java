package dstu.csae.auth.graphic.repository;


import java.util.UUID;

import dstu.csae.auth.graphic.model.Account;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AccountRepository extends JpaRepository<Account, UUID> {
    boolean existsByLogin(String login);
    boolean existsByEmail(String email);
    Account findByLogin(String login);
}
