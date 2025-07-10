package dstu.csae.auth.graphic.repository;

import dstu.csae.auth.graphic.model.AccountPoint;
import dstu.csae.auth.graphic.model.AccountPointId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface AccountPointRepository extends JpaRepository<AccountPoint, AccountPointId> {
    List<AccountPoint> findByAccountId(UUID accountId);
}

